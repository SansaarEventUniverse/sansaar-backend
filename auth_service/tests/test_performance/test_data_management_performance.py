import time
from datetime import timedelta
from unittest.mock import patch

import pytest
from django.utils import timezone

from application.anonymize_account_service import AnonymizeUserDataService
from application.audit_log_retention_service import AuditLogRetentionService
from domain.audit_log_model import AuditEventType
from domain.models import AccountDeactivation, AuditLog, User


@pytest.mark.django_db
class TestAnonymizationPerformance:
    @patch("application.anonymize_account_service.EventPublisher.publish_account_anonymized")
    def test_single_user_anonymization_performance(self, mock_publish):
        user = User.objects.create_user(
            email="perf@example.com", password="TestPass123!", first_name="Perf", last_name="User"
        )
        user.is_active = False
        user.save()

        deactivation = AccountDeactivation.objects.create(user_id=str(user.id))
        deactivation.mark_permanently_deactivated()

        service = AnonymizeUserDataService()

        start_time = time.time()
        service.anonymize(str(user.id))
        end_time = time.time()

        # Should complete in under 1 second
        assert (end_time - start_time) < 1.0

    @patch("application.anonymize_account_service.EventPublisher.publish_account_anonymized")
    def test_bulk_anonymization_performance(self, mock_publish):
        users = []
        for i in range(10):
            user = User.objects.create_user(
                email=f"bulk{i}@example.com", password="TestPass123!", first_name=f"User{i}", last_name="Test"
            )
            user.is_active = False
            user.save()

            deactivation = AccountDeactivation.objects.create(user_id=str(user.id))
            deactivation.mark_permanently_deactivated()
            users.append(user)

        service = AnonymizeUserDataService()

        start_time = time.time()
        for user in users:
            service.anonymize(str(user.id))
        end_time = time.time()

        # Should complete 10 anonymizations in under 5 seconds
        assert (end_time - start_time) < 5.0


@pytest.mark.django_db
class TestDataExportPerformance:
    def test_audit_log_query_performance(self):
        user = User.objects.create_user(
            email="export@example.com", password="TestPass123!", first_name="Export", last_name="User"
        )

        # Create 100 audit logs
        for i in range(100):
            AuditLog.objects.create(event_type=AuditEventType.LOGIN, user_id=str(user.id), success=True)

        start_time = time.time()
        logs = list(AuditLog.objects.filter(user_id=str(user.id)))
        end_time = time.time()

        assert len(logs) == 100
        # Should query 100 logs in under 0.5 seconds
        assert (end_time - start_time) < 0.5

    def test_user_data_export_performance(self):
        user = User.objects.create_user(
            email="data@example.com", password="TestPass123!", first_name="Data", last_name="User"
        )

        # Create audit logs
        for i in range(50):
            AuditLog.objects.create(event_type=AuditEventType.LOGIN, user_id=str(user.id), success=True)

        start_time = time.time()
        user_data = {
            "personal_data": {"email": user.email, "first_name": user.first_name, "last_name": user.last_name},
            "audit_logs": list(AuditLog.objects.filter(user_id=str(user.id)).values()),
        }
        end_time = time.time()

        assert len(user_data["audit_logs"]) == 50
        # Should export data in under 0.5 seconds
        assert (end_time - start_time) < 0.5


@pytest.mark.django_db
class TestRetentionPolicyPerformance:
    @patch("infrastructure.services.audit_log_archival_service.boto3")
    def test_log_archival_performance(self, mock_boto3):
        mock_s3 = mock_boto3.client.return_value

        # Create 50 old logs
        time_now = timezone.now()
        for i in range(50):
            log = AuditLog.objects.create(event_type=AuditEventType.LOGIN, user_id=str(i), success=True)
            AuditLog.objects.filter(id=log.id).update(created_at=time_now - timedelta(days=100))

        service = AuditLogRetentionService()

        start_time = time.time()
        result = service.archive_and_delete_logs()
        end_time = time.time()

        # Should process 50 logs in under 2 seconds
        assert (end_time - start_time) < 2.0

    def test_retention_policy_query_performance(self):
        # Create logs with different event types
        time_now = timezone.now()
        for event_type in [AuditEventType.LOGIN, AuditEventType.REGISTRATION, AuditEventType.PASSWORD_RESET]:
            for i in range(20):
                log = AuditLog.objects.create(event_type=event_type, user_id=str(i), success=True)
                AuditLog.objects.filter(id=log.id).update(created_at=time_now - timedelta(days=100))

        service = AuditLogRetentionService()

        start_time = time.time()
        logs = service.archival_service.get_logs_for_deletion()
        end_time = time.time()

        # Should query retention policy in under 0.5 seconds
        assert (end_time - start_time) < 0.5


@pytest.mark.django_db
class TestSecurityMonitoringPerformance:
    def test_failed_login_monitoring_performance(self):
        from infrastructure.services.security_monitoring_service import SecurityMonitoringService

        # Create 100 failed login attempts
        time_now = timezone.now()
        for i in range(100):
            log = AuditLog.objects.create(event_type=AuditEventType.LOGIN, user_id="1", success=False)
            AuditLog.objects.filter(id=log.id).update(created_at=time_now - timedelta(minutes=i % 15))

        service = SecurityMonitoringService()

        start_time = time.time()
        with patch.object(service.alert_service, "send_alert"):
            service.monitor_failed_logins("1")
        end_time = time.time()

        # Should monitor in under 0.5 seconds
        assert (end_time - start_time) < 0.5

    def test_system_wide_monitoring_performance(self):
        from application.security_monitoring_application_service import SecurityMonitoringApplicationService

        # Create various security events
        time_now = timezone.now()
        for i in range(50):
            log = AuditLog.objects.create(event_type=AuditEventType.ACCOUNT_LOCKED, user_id=str(i), success=True)
            AuditLog.objects.filter(id=log.id).update(created_at=time_now - timedelta(minutes=i % 60))

        service = SecurityMonitoringApplicationService()

        start_time = time.time()
        with patch("infrastructure.services.security_monitoring_service.AlertService.send_alert"):
            service.monitor_system_security()
        end_time = time.time()

        # Should monitor system in under 1 second
        assert (end_time - start_time) < 1.0
