from datetime import timedelta
from unittest.mock import MagicMock, patch

import pytest
from django.utils import timezone

from domain.audit_log_model import AuditEventType
from domain.models import AuditLog
from infrastructure.retention_policy import AuditLogRetentionPolicy
from infrastructure.services.audit_log_archival_service import AuditLogArchivalService
from infrastructure.tasks.audit_log_tasks import archive_audit_logs, delete_expired_audit_logs


@pytest.mark.django_db
class TestAuditLogArchival:
    def setup_method(self):
        self.service = AuditLogArchivalService()

    def test_get_logs_for_archival(self):
        old_date = timezone.now() - timedelta(days=100)
        recent_date = timezone.now() - timedelta(days=10)

        log1 = AuditLog.objects.create(
            event_type=AuditEventType.LOGIN, user_id="1", success=True
        )
        AuditLog.objects.filter(id=log1.id).update(created_at=old_date)

        log2 = AuditLog.objects.create(
            event_type=AuditEventType.LOGIN, user_id="2", success=True
        )
        AuditLog.objects.filter(id=log2.id).update(created_at=recent_date)

        logs = self.service.get_logs_for_archival()
        assert logs.count() == 1
        assert logs.first().user_id == "1"

    def test_get_logs_for_deletion(self):
        old_login = timezone.now() - timedelta(days=100)
        recent_registration = timezone.now() - timedelta(days=100)

        log1 = AuditLog.objects.create(
            event_type=AuditEventType.LOGIN, user_id="1", success=True
        )
        AuditLog.objects.filter(id=log1.id).update(created_at=old_login)

        log2 = AuditLog.objects.create(
            event_type=AuditEventType.REGISTRATION, user_id="2", success=True
        )
        AuditLog.objects.filter(id=log2.id).update(created_at=recent_registration)

        logs = self.service.get_logs_for_deletion()
        # LOGIN has 90 day retention, so it should be deleted
        # REGISTRATION has 7 year retention, so it should NOT be deleted
        assert len(logs) == 1
        assert logs[0].event_type == AuditEventType.LOGIN

    @patch("infrastructure.services.audit_log_archival_service.boto3")
    def test_archive_logs_success(self, mock_boto3):
        mock_s3 = MagicMock()
        mock_boto3.client.return_value = mock_s3

        log = AuditLog.objects.create(
            event_type=AuditEventType.LOGIN, user_id="1", success=True
        )

        service = AuditLogArchivalService()
        count = service.archive_logs([log])

        assert count == 1
        mock_s3.put_object.assert_called_once()

    @patch("infrastructure.services.audit_log_archival_service.boto3")
    def test_archive_logs_empty_list(self, mock_boto3):
        service = AuditLogArchivalService()
        count = service.archive_logs([])
        assert count == 0

    def test_delete_logs(self):
        log1 = AuditLog.objects.create(
            event_type=AuditEventType.LOGIN, user_id="1", success=True
        )
        log2 = AuditLog.objects.create(
            event_type=AuditEventType.LOGIN, user_id="2", success=True
        )

        deleted = self.service.delete_logs([log1.id, log2.id])
        assert deleted == 2
        assert AuditLog.objects.count() == 0

    def test_delete_logs_empty_list(self):
        deleted = self.service.delete_logs([])
        assert deleted == 0


@pytest.mark.django_db
class TestRetentionPolicy:
    def test_retention_periods_defined(self):
        assert AuditLogRetentionPolicy.get_retention_period("REGISTRATION") == timedelta(days=2555)
        assert AuditLogRetentionPolicy.get_retention_period("LOGIN") == timedelta(days=90)
        assert AuditLogRetentionPolicy.get_retention_period("ACCOUNT_ANONYMIZED") == timedelta(days=2555)

    def test_default_retention_period(self):
        assert AuditLogRetentionPolicy.get_retention_period("UNKNOWN_EVENT") == timedelta(days=365)


@pytest.mark.django_db
class TestAuditLogTasks:
    @patch("infrastructure.tasks.audit_log_tasks.AuditLogArchivalService")
    def test_archive_audit_logs_task(self, mock_service_class):
        mock_service = MagicMock()
        mock_service_class.return_value = mock_service

        mock_log = MagicMock()
        mock_log.id = 1
        mock_service.get_logs_for_archival.return_value = [mock_log]
        mock_service.archive_logs.return_value = 1
        mock_service.delete_logs.return_value = 1

        result = archive_audit_logs()

        assert result["archived"] == 1
        assert result["deleted"] == 1
        mock_service.archive_logs.assert_called_once()
        mock_service.delete_logs.assert_called_once_with([1])

    @patch("infrastructure.tasks.audit_log_tasks.AuditLogArchivalService")
    def test_delete_expired_audit_logs_task(self, mock_service_class):
        mock_service = MagicMock()
        mock_service_class.return_value = mock_service

        mock_log = MagicMock()
        mock_log.id = 1
        mock_service.get_logs_for_deletion.return_value = [mock_log]
        mock_service.delete_logs.return_value = 1

        result = delete_expired_audit_logs()

        assert result["deleted"] == 1
        mock_service.delete_logs.assert_called_once_with([1])


@pytest.mark.django_db
class TestS3Archival:
    @patch("infrastructure.services.audit_log_archival_service.boto3")
    def test_s3_archival_with_glacier_storage(self, mock_boto3):
        mock_s3 = MagicMock()
        mock_boto3.client.return_value = mock_s3

        log = AuditLog.objects.create(
            event_type=AuditEventType.REGISTRATION, user_id="1", success=True
        )

        service = AuditLogArchivalService()
        service.archive_logs([log])

        call_args = mock_s3.put_object.call_args
        assert call_args[1]["StorageClass"] == "GLACIER"
        assert "archived/" in call_args[1]["Key"]

    @patch("infrastructure.services.audit_log_archival_service.boto3")
    def test_s3_archival_failure_handling(self, mock_boto3):
        mock_s3 = MagicMock()
        mock_s3.put_object.side_effect = Exception("S3 Error")
        mock_boto3.client.return_value = mock_s3

        log = AuditLog.objects.create(
            event_type=AuditEventType.LOGIN, user_id="1", success=True
        )

        service = AuditLogArchivalService()
        count = service.archive_logs([log])

        assert count == 0


@pytest.mark.django_db
class TestLogDeletionValidation:
    def test_deletion_only_after_archival(self):
        old_date = timezone.now() - timedelta(days=100)
        log = AuditLog.objects.create(
            event_type=AuditEventType.LOGIN, user_id="1", success=True
        )
        AuditLog.objects.filter(id=log.id).update(created_at=old_date)

        service = AuditLogArchivalService()
        logs = service.get_logs_for_archival()
        assert logs.count() == 1

        # Simulate archival
        service.delete_logs([log.id])
        assert AuditLog.objects.count() == 0

    def test_retention_policy_enforcement(self):
        login_cutoff = timezone.now() - timedelta(days=91)
        registration_cutoff = timezone.now() - timedelta(days=2556)

        log1 = AuditLog.objects.create(
            event_type=AuditEventType.LOGIN, user_id="1", success=True
        )
        AuditLog.objects.filter(id=log1.id).update(created_at=login_cutoff)

        log2 = AuditLog.objects.create(
            event_type=AuditEventType.REGISTRATION, user_id="2", success=True
        )
        AuditLog.objects.filter(id=log2.id).update(created_at=registration_cutoff)

        service = AuditLogArchivalService()
        logs = service.get_logs_for_deletion()

        assert len(logs) == 2
