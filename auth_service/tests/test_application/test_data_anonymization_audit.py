from unittest.mock import patch

import pytest

from application.anonymize_account_service import AnonymizeUserDataService
from domain.audit_log_model import AuditEventType, AuditLog
from domain.models import AccountDeactivation, User


@pytest.mark.django_db
class TestDataAnonymizationAudit:
    def setup_method(self):
        self.service = AnonymizeUserDataService()
        self.user = User.objects.create_user(
            email="test@example.com", password="TestPass123!", first_name="John", last_name="Doe"
        )
        self.user.is_active = False
        self.user.save()

    def test_audit_log_preserved_after_anonymization(self):
        deactivation = AccountDeactivation.objects.create(user_id=str(self.user.id))
        deactivation.mark_permanently_deactivated()

        with patch.object(self.service.event_publisher, "publish_account_anonymized"):
            self.service.anonymize(str(self.user.id))

        # Verify audit log exists
        audit_log = AuditLog.objects.filter(user_id=str(self.user.id), event_type=AuditEventType.ACCOUNT_ANONYMIZED)
        assert audit_log.exists()
        assert audit_log.count() == 1

        log = audit_log.first()
        assert log.user_id == str(self.user.id)
        assert log.success is True
        assert "original_email" in log.metadata
        assert log.metadata["original_email"] == "test@example.com"

    def test_user_id_reference_maintained_in_audit_logs(self):
        deactivation = AccountDeactivation.objects.create(user_id=str(self.user.id))
        deactivation.mark_permanently_deactivated()

        with patch.object(self.service.event_publisher, "publish_account_anonymized"):
            self.service.anonymize(str(self.user.id))

        self.user.refresh_from_db()

        # User data is anonymized
        assert self.user.email.startswith("deleted_")

        # But audit log still references original user_id
        audit_log = AuditLog.objects.get(user_id=str(self.user.id), event_type=AuditEventType.ACCOUNT_ANONYMIZED)
        assert audit_log.user_id == str(self.user.id)

    def test_compliance_audit_trail(self):
        deactivation = AccountDeactivation.objects.create(user_id=str(self.user.id))
        deactivation.mark_permanently_deactivated()

        with patch.object(self.service.event_publisher, "publish_account_anonymized"):
            self.service.anonymize(str(self.user.id))

        audit_log = AuditLog.objects.get(user_id=str(self.user.id), event_type=AuditEventType.ACCOUNT_ANONYMIZED)

        # Verify compliance fields
        assert audit_log.event_type == AuditEventType.ACCOUNT_ANONYMIZED
        assert audit_log.user_id == str(self.user.id)
        assert audit_log.created_at is not None
        assert audit_log.success is True
        assert "original_email" in audit_log.metadata
        assert "anonymized_email" in audit_log.metadata

    def test_anonymization_tracking(self):
        deactivation = AccountDeactivation.objects.create(user_id=str(self.user.id))
        deactivation.mark_permanently_deactivated()

        with patch.object(self.service.event_publisher, "publish_account_anonymized"):
            result = self.service.anonymize(str(self.user.id))

        deactivation.refresh_from_db()

        # Verify anonymization tracking in deactivation record
        assert deactivation.is_anonymized is True
        assert deactivation.anonymized_at is not None

        # Verify audit log tracks anonymization
        audit_log = AuditLog.objects.get(user_id=str(self.user.id), event_type=AuditEventType.ACCOUNT_ANONYMIZED)
        assert audit_log.metadata["anonymized_email"] == result["anonymized_email"]

    def test_audit_logs_not_anonymized(self):
        # Create some audit logs before anonymization
        AuditLog.objects.create(
            event_type=AuditEventType.LOGIN,
            user_id=str(self.user.id),
            success=True,
            metadata={"email": "test@example.com"},
        )

        deactivation = AccountDeactivation.objects.create(user_id=str(self.user.id))
        deactivation.mark_permanently_deactivated()

        with patch.object(self.service.event_publisher, "publish_account_anonymized"):
            self.service.anonymize(str(self.user.id))

        # Verify old audit logs are preserved
        login_log = AuditLog.objects.get(user_id=str(self.user.id), event_type=AuditEventType.LOGIN)
        assert login_log.user_id == str(self.user.id)
        assert login_log.metadata["email"] == "test@example.com"

        # Verify new anonymization log exists
        anon_log = AuditLog.objects.get(user_id=str(self.user.id), event_type=AuditEventType.ACCOUNT_ANONYMIZED)
        assert anon_log.user_id == str(self.user.id)

    def test_data_retention_policy_compliance(self):
        deactivation = AccountDeactivation.objects.create(user_id=str(self.user.id))
        deactivation.mark_permanently_deactivated()

        with patch.object(self.service.event_publisher, "publish_account_anonymized"):
            self.service.anonymize(str(self.user.id))

        # Verify user data is anonymized (GDPR right to be forgotten)
        self.user.refresh_from_db()
        assert self.user.email.startswith("deleted_")
        assert self.user.first_name == "Deleted"
        assert self.user.last_name == "User"

        # Verify audit trail is preserved (compliance requirement)
        audit_logs = AuditLog.objects.filter(user_id=str(self.user.id))
        assert audit_logs.exists()
        assert audit_logs.filter(event_type=AuditEventType.ACCOUNT_ANONYMIZED).exists()

    def test_multiple_anonymizations_tracked(self):
        user2 = User.objects.create_user(
            email="test2@example.com", password="TestPass123!", first_name="Jane", last_name="Smith"
        )
        user2.is_active = False
        user2.save()

        deactivation1 = AccountDeactivation.objects.create(user_id=str(self.user.id))
        deactivation1.mark_permanently_deactivated()

        deactivation2 = AccountDeactivation.objects.create(user_id=str(user2.id))
        deactivation2.mark_permanently_deactivated()

        with patch.object(self.service.event_publisher, "publish_account_anonymized"):
            self.service.anonymize(str(self.user.id))
            self.service.anonymize(str(user2.id))

        # Verify separate audit logs for each user
        audit_logs = AuditLog.objects.filter(event_type=AuditEventType.ACCOUNT_ANONYMIZED)
        assert audit_logs.count() == 2

        user1_log = audit_logs.get(user_id=str(self.user.id))
        user2_log = audit_logs.get(user_id=str(user2.id))

        assert user1_log.metadata["original_email"] == "test@example.com"
        assert user2_log.metadata["original_email"] == "test2@example.com"
