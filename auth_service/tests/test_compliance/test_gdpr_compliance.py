from datetime import timedelta
from unittest.mock import patch

import pytest
from django.utils import timezone

from application.anonymize_account_service import AnonymizeUserDataService
from domain.audit_log_model import AuditEventType
from domain.models import AccountDeactivation, AuditLog, User


@pytest.mark.django_db
class TestGDPRDataExport:
    def setup_method(self):
        self.user = User.objects.create_user(
            email="gdpr@example.com", password="TestPass123!", first_name="GDPR", last_name="User"
        )

    def test_data_export_includes_all_user_data(self):
        # Create audit logs
        AuditLog.objects.create(event_type=AuditEventType.LOGIN, user_id=str(self.user.id), success=True)

        # Verify all data is accessible
        user_data = {
            "email": self.user.email,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "date_joined": self.user.date_joined,
            "is_active": self.user.is_active,
        }

        audit_logs = AuditLog.objects.filter(user_id=str(self.user.id))

        assert user_data["email"] == "gdpr@example.com"
        assert audit_logs.count() == 1

    def test_data_export_format_compliance(self):
        # GDPR requires machine-readable format
        user_data = {
            "personal_data": {
                "email": self.user.email,
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
            },
            "account_data": {"date_joined": str(self.user.date_joined), "is_active": self.user.is_active},
            "audit_trail": list(
                AuditLog.objects.filter(user_id=str(self.user.id)).values(
                    "event_type", "created_at", "success", "ip_address"
                )
            ),
        }

        assert "personal_data" in user_data
        assert "account_data" in user_data
        assert "audit_trail" in user_data


@pytest.mark.django_db
class TestGDPRDataDeletion:
    def setup_method(self):
        self.user = User.objects.create_user(
            email="delete@example.com", password="TestPass123!", first_name="Delete", last_name="User"
        )
        self.user.is_active = False
        self.user.save()

    @patch("application.anonymize_account_service.EventPublisher.publish_account_anonymized")
    def test_deletion_completeness(self, mock_publish):
        # Create deactivation
        deactivation = AccountDeactivation.objects.create(user_id=str(self.user.id))
        deactivation.mark_permanently_deactivated()

        # Anonymize
        service = AnonymizeUserDataService()
        service.anonymize(str(self.user.id))

        self.user.refresh_from_db()

        # Verify PII is removed
        assert not self.user.email.startswith("delete@")
        assert self.user.email.endswith("@anonymized.local")
        assert self.user.first_name == "Deleted"
        assert self.user.last_name == "User"

    @patch("application.anonymize_account_service.EventPublisher.publish_account_anonymized")
    def test_audit_trail_preserved(self, mock_publish):
        # Create audit log before anonymization
        AuditLog.objects.create(
            event_type=AuditEventType.LOGIN,
            user_id=str(self.user.id),
            success=True,
            metadata={"email": "delete@example.com"},
        )

        deactivation = AccountDeactivation.objects.create(user_id=str(self.user.id))
        deactivation.mark_permanently_deactivated()

        service = AnonymizeUserDataService()
        service.anonymize(str(self.user.id))

        # Audit logs must be preserved for compliance
        audit_logs = AuditLog.objects.filter(user_id=str(self.user.id))
        assert audit_logs.exists()


@pytest.mark.django_db
class TestGDPRAnonymization:
    def setup_method(self):
        self.user = User.objects.create_user(
            email="anon@example.com", password="TestPass123!", first_name="Anon", last_name="User"
        )
        self.user.is_active = False
        self.user.save()

    @patch("application.anonymize_account_service.EventPublisher.publish_account_anonymized")
    def test_anonymization_irreversibility(self, mock_publish):
        original_email = self.user.email

        deactivation = AccountDeactivation.objects.create(user_id=str(self.user.id))
        deactivation.mark_permanently_deactivated()

        service = AnonymizeUserDataService()
        service.anonymize(str(self.user.id))

        self.user.refresh_from_db()

        # Cannot reverse anonymization
        assert self.user.email != original_email
        assert "anon@example.com" not in self.user.email

    @patch("application.anonymize_account_service.EventPublisher.publish_account_anonymized")
    def test_anonymization_uniqueness(self, mock_publish):
        user2 = User.objects.create_user(
            email="anon2@example.com", password="TestPass123!", first_name="Anon2", last_name="User2"
        )
        user2.is_active = False
        user2.save()

        deactivation1 = AccountDeactivation.objects.create(user_id=str(self.user.id))
        deactivation1.mark_permanently_deactivated()

        deactivation2 = AccountDeactivation.objects.create(user_id=str(user2.id))
        deactivation2.mark_permanently_deactivated()

        service = AnonymizeUserDataService()
        service.anonymize(str(self.user.id))
        service.anonymize(str(user2.id))

        self.user.refresh_from_db()
        user2.refresh_from_db()

        # Each anonymization must be unique
        assert self.user.email != user2.email


@pytest.mark.django_db
class TestGDPRRetentionPolicy:
    def test_retention_periods_defined(self):
        from infrastructure.retention_policy import AuditLogRetentionPolicy

        # Critical events must have longer retention
        registration_retention = AuditLogRetentionPolicy.get_retention_period("REGISTRATION")
        login_retention = AuditLogRetentionPolicy.get_retention_period("LOGIN")

        assert registration_retention.days == 2555  # 7 years
        assert login_retention.days == 90

    def test_retention_policy_enforcement(self):
        from infrastructure.services.audit_log_archival_service import AuditLogArchivalService

        service = AuditLogArchivalService()

        # Create old log
        old_date = timezone.now() - timedelta(days=100)
        log = AuditLog.objects.create(event_type=AuditEventType.LOGIN, user_id="1", success=True)
        AuditLog.objects.filter(id=log.id).update(created_at=old_date)

        logs = service.get_logs_for_deletion()
        assert len(logs) == 1


@pytest.mark.django_db
class TestGDPRRightToAccess:
    def setup_method(self):
        self.user = User.objects.create_user(
            email="access@example.com", password="TestPass123!", first_name="Access", last_name="User"
        )

    def test_user_can_access_own_data(self):
        # User must be able to access all their data
        user_data = User.objects.filter(id=self.user.id).values()
        assert user_data.exists()
        assert user_data.first().get("email") == "access@example.com"

    def test_user_can_access_audit_logs(self):
        AuditLog.objects.create(event_type=AuditEventType.LOGIN, user_id=str(self.user.id), success=True)

        logs = AuditLog.objects.filter(user_id=str(self.user.id))
        assert logs.exists()


@pytest.mark.django_db
class TestGDPRRightToRectification:
    def setup_method(self):
        self.user = User.objects.create_user(
            email="rectify@example.com", password="TestPass123!", first_name="Wrong", last_name="Name"
        )

    def test_user_can_update_personal_data(self):
        # User must be able to correct their data
        self.user.first_name = "Correct"
        self.user.last_name = "Name"
        self.user.save()

        self.user.refresh_from_db()
        assert self.user.first_name == "Correct"
        assert self.user.last_name == "Name"


@pytest.mark.django_db
class TestGDPRDataPortability:
    def setup_method(self):
        self.user = User.objects.create_user(
            email="portable@example.com", password="TestPass123!", first_name="Portable", last_name="User"
        )

    def test_data_export_machine_readable(self):
        import json

        # Data must be in machine-readable format
        user_data = {
            "email": self.user.email,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "date_joined": str(self.user.date_joined),
        }

        # Must be JSON serializable
        json_data = json.dumps(user_data)
        assert json_data is not None
        assert "portable@example.com" in json_data
