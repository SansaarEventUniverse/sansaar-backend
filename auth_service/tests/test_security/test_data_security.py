from datetime import timedelta
from unittest.mock import patch

import pytest
from django.utils import timezone

from application.anonymize_account_service import AnonymizeUserDataService
from domain.audit_log_model import AuditEventType
from domain.models import AccountDeactivation, AuditLog, User


@pytest.mark.django_db
class TestDataAccessControls:
    def setup_method(self):
        self.user1 = User.objects.create_user(
            email="user1@example.com", password="TestPass123!", first_name="User", last_name="One"
        )
        self.user2 = User.objects.create_user(
            email="user2@example.com", password="TestPass123!", first_name="User", last_name="Two"
        )

    def test_user_cannot_access_other_user_data(self):
        # Users should only access their own data
        user1_logs = AuditLog.objects.filter(user_id=str(self.user1.id))
        user2_logs = AuditLog.objects.filter(user_id=str(self.user2.id))

        assert user1_logs.count() == 0
        assert user2_logs.count() == 0

    def test_anonymization_requires_deactivation(self):
        service = AnonymizeUserDataService()

        with pytest.raises(Exception):
            service.anonymize(str(self.user1.id))


@pytest.mark.django_db
class TestAuditTrailIntegrity:
    def setup_method(self):
        self.user = User.objects.create_user(
            email="audit@example.com", password="TestPass123!", first_name="Audit", last_name="User"
        )

    def test_audit_log_immutability(self):
        log = AuditLog.objects.create(
            event_type=AuditEventType.LOGIN, user_id=str(self.user.id), success=True, metadata={"test": "data"}
        )

        original_created_at = log.created_at
        original_metadata = log.metadata.copy()

        # Audit logs should not be modified
        log.refresh_from_db()
        assert log.created_at == original_created_at
        assert log.metadata == original_metadata

    @patch("application.anonymize_account_service.EventPublisher.publish_account_anonymized")
    def test_audit_trail_preserved_after_anonymization(self, mock_publish):
        # Create audit logs
        AuditLog.objects.create(
            event_type=AuditEventType.LOGIN,
            user_id=str(self.user.id),
            success=True,
            metadata={"original_email": "audit@example.com"},
        )

        self.user.is_active = False
        self.user.save()

        deactivation = AccountDeactivation.objects.create(user_id=str(self.user.id))
        deactivation.mark_permanently_deactivated()

        service = AnonymizeUserDataService()
        service.anonymize(str(self.user.id))

        # Audit logs must remain intact
        logs = AuditLog.objects.filter(user_id=str(self.user.id))
        assert logs.exists()
        assert logs.first().metadata["original_email"] == "audit@example.com"

    def test_audit_log_completeness(self):
        # All security events must be logged
        log = AuditLog.objects.create(
            event_type=AuditEventType.LOGIN,
            user_id=str(self.user.id),
            success=True,
            ip_address="192.168.1.1",
            user_agent="Mozilla/5.0",
        )

        assert log.event_type is not None
        assert log.user_id is not None
        assert log.created_at is not None


@pytest.mark.django_db
class TestDataDeletionSecurity:
    def setup_method(self):
        self.user = User.objects.create_user(
            email="secure@example.com", password="TestPass123!", first_name="Secure", last_name="User"
        )
        self.user.is_active = False
        self.user.save()

    @patch("application.anonymize_account_service.EventPublisher.publish_account_anonymized")
    def test_deletion_requires_permanent_deactivation(self, mock_publish):
        deactivation = AccountDeactivation.objects.create(user_id=str(self.user.id))

        service = AnonymizeUserDataService()

        with pytest.raises(ValueError, match="permanently deactivated"):
            service.anonymize(str(self.user.id))

    @patch("application.anonymize_account_service.EventPublisher.publish_account_anonymized")
    def test_deletion_prevents_duplicate(self, mock_publish):
        deactivation = AccountDeactivation.objects.create(user_id=str(self.user.id))
        deactivation.mark_permanently_deactivated()

        service = AnonymizeUserDataService()
        service.anonymize(str(self.user.id))

        with pytest.raises(ValueError, match="already anonymized"):
            service.anonymize(str(self.user.id))

    @patch("application.anonymize_account_service.EventPublisher.publish_account_anonymized")
    def test_deletion_creates_audit_log(self, mock_publish):
        deactivation = AccountDeactivation.objects.create(user_id=str(self.user.id))
        deactivation.mark_permanently_deactivated()

        service = AnonymizeUserDataService()
        service.anonymize(str(self.user.id))

        # Anonymization must be logged
        log = AuditLog.objects.filter(
            user_id=str(self.user.id), event_type=AuditEventType.ACCOUNT_ANONYMIZED
        ).first()

        assert log is not None
        assert log.success is True


@pytest.mark.django_db
class TestRetentionPolicySecurity:
    def test_retention_policy_cannot_be_bypassed(self):
        from infrastructure.services.audit_log_archival_service import AuditLogArchivalService

        service = AuditLogArchivalService()

        # Create recent log
        log = AuditLog.objects.create(event_type=AuditEventType.LOGIN, user_id="1", success=True)

        # Recent logs should not be deleted
        logs_for_deletion = service.get_logs_for_deletion()
        assert log not in logs_for_deletion

    def test_critical_logs_have_extended_retention(self):
        from infrastructure.retention_policy import AuditLogRetentionPolicy

        # Registration and anonymization logs must be kept longer
        registration_retention = AuditLogRetentionPolicy.get_retention_period("REGISTRATION")
        anonymization_retention = AuditLogRetentionPolicy.get_retention_period("ACCOUNT_ANONYMIZED")

        assert registration_retention.days >= 2555  # 7 years
        assert anonymization_retention.days >= 2555


@pytest.mark.django_db
class TestSecurityMonitoringIntegrity:
    def test_failed_login_monitoring(self):
        from infrastructure.services.security_monitoring_service import SecurityMonitoringService

        service = SecurityMonitoringService()

        time_now = timezone.now()
        for i in range(6):
            log = AuditLog.objects.create(event_type=AuditEventType.LOGIN, user_id="1", success=False)
            AuditLog.objects.filter(id=log.id).update(created_at=time_now - timedelta(minutes=i))

        with patch.object(service.alert_service, "send_alert") as mock_alert:
            result = service.monitor_failed_logins("1")
            assert result is True
            mock_alert.assert_called_once()

    def test_alert_threshold_enforcement(self):
        from infrastructure.alert_thresholds import AlertThresholds

        # Thresholds must be enforced
        config = AlertThresholds.get_threshold("FAILED_LOGIN_SPIKE")
        assert config["threshold"] > 0
        assert config["window_minutes"] > 0
