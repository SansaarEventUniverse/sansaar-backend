from datetime import timedelta
from unittest.mock import MagicMock, patch

import pytest
from django.utils import timezone

from application.audit_log_retention_service import AuditLogRetentionService
from domain.audit_log_model import AuditEventType
from domain.models import AuditLog


@pytest.mark.django_db
class TestAuditLogRetentionService:
    def setup_method(self):
        self.service = AuditLogRetentionService()

    @patch("application.audit_log_retention_service.AuditLogArchivalService")
    def test_archive_and_delete_logs_success(self, mock_archival_class):
        mock_archival = MagicMock()
        mock_archival_class.return_value = mock_archival

        mock_log = MagicMock()
        mock_log.id = 1
        mock_archival.get_logs_for_archival.return_value = [mock_log]
        mock_archival.archive_logs.return_value = 1
        mock_archival.delete_logs.return_value = 1

        service = AuditLogRetentionService()
        result = service.archive_and_delete_logs()

        assert result["archived"] == 1
        assert result["deleted"] == 1

    @patch("application.audit_log_retention_service.AuditLogArchivalService")
    def test_archive_and_delete_logs_no_logs(self, mock_archival_class):
        mock_archival = MagicMock()
        mock_archival_class.return_value = mock_archival
        mock_archival.get_logs_for_archival.return_value = []

        service = AuditLogRetentionService()
        result = service.archive_and_delete_logs()

        assert result["archived"] == 0
        assert result["deleted"] == 0

    @patch("application.audit_log_retention_service.AuditLogArchivalService")
    def test_delete_expired_logs_success(self, mock_archival_class):
        mock_archival = MagicMock()
        mock_archival_class.return_value = mock_archival

        mock_log = MagicMock()
        mock_log.id = 1
        mock_archival.get_logs_for_deletion.return_value = [mock_log]
        mock_archival.delete_logs.return_value = 1

        service = AuditLogRetentionService()
        result = service.delete_expired_logs()

        assert result["deleted"] == 1

    @patch("application.audit_log_retention_service.AuditLogArchivalService")
    def test_delete_expired_logs_no_logs(self, mock_archival_class):
        mock_archival = MagicMock()
        mock_archival_class.return_value = mock_archival
        mock_archival.get_logs_for_deletion.return_value = []

        service = AuditLogRetentionService()
        result = service.delete_expired_logs()

        assert result["deleted"] == 0

    def test_validate_retention_policy(self):
        result = self.service.validate_retention_policy(AuditEventType.LOGIN)
        assert result["event_type"] == AuditEventType.LOGIN
        assert result["retention_days"] == 90
        assert result["valid"] is True

    def test_validate_retention_policy_registration(self):
        result = self.service.validate_retention_policy(AuditEventType.REGISTRATION)
        assert result["event_type"] == AuditEventType.REGISTRATION
        assert result["retention_days"] == 2555
        assert result["valid"] is True

    def test_validate_retention_policy_unknown_event(self):
        result = self.service.validate_retention_policy("UNKNOWN_EVENT")
        assert result["event_type"] == "UNKNOWN_EVENT"
        assert result["retention_days"] == 365
        assert result["valid"] is True


@pytest.mark.django_db
class TestRetentionPolicyLogic:
    def test_archival_validation(self):
        service = AuditLogRetentionService()

        old_date = timezone.now() - timedelta(days=100)
        log = AuditLog.objects.create(
            event_type=AuditEventType.LOGIN, user_id="1", success=True
        )
        AuditLog.objects.filter(id=log.id).update(created_at=old_date)

        logs = service.archival_service.get_logs_for_archival()
        assert logs.count() == 1

    def test_deletion_safety_checks(self):
        service = AuditLogRetentionService()

        recent_date = timezone.now() - timedelta(days=10)
        log = AuditLog.objects.create(
            event_type=AuditEventType.LOGIN, user_id="1", success=True
        )
        AuditLog.objects.filter(id=log.id).update(created_at=recent_date)

        logs = service.archival_service.get_logs_for_deletion()
        assert len(logs) == 0


@pytest.mark.django_db
class TestRetentionServiceIntegration:
    def test_full_archival_workflow(self):
        service = AuditLogRetentionService()

        old_date = timezone.now() - timedelta(days=100)
        log = AuditLog.objects.create(
            event_type=AuditEventType.LOGIN, user_id="1", success=True
        )
        AuditLog.objects.filter(id=log.id).update(created_at=old_date)

        with patch.object(service.archival_service, "archive_logs", return_value=1):
            result = service.archive_and_delete_logs()
            assert result["archived"] == 1
            assert result["deleted"] == 1

    def test_retention_policy_configuration(self):
        service = AuditLogRetentionService()

        # Test all event types have retention policies
        for event_type in [
            AuditEventType.REGISTRATION,
            AuditEventType.LOGIN,
            AuditEventType.ACCOUNT_ANONYMIZED,
        ]:
            result = service.validate_retention_policy(event_type)
            assert result["valid"] is True
            assert result["retention_days"] > 0
