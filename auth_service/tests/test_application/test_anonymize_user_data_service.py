import uuid
from unittest.mock import MagicMock, patch

import pytest
from django.utils import timezone

from application.anonymize_account_service import AnonymizeUserDataService
from domain.models import AccountDeactivation, User


@pytest.mark.django_db
class TestAnonymizeUserDataService:
    def setup_method(self):
        self.service = AnonymizeUserDataService()
        self.user = User.objects.create_user(
            email="test@example.com", password="TestPass123!", first_name="John", last_name="Doe"
        )
        self.user.is_active = False
        self.user.save()

    def test_anonymize_success(self):
        deactivation = AccountDeactivation.objects.create(user_id=str(self.user.id))
        deactivation.mark_permanently_deactivated()

        with patch.object(self.service.event_publisher, "publish_account_anonymized") as mock_publish:
            result = self.service.anonymize(str(self.user.id))

            self.user.refresh_from_db()
            deactivation.refresh_from_db()

            assert result["message"] == "Account anonymized successfully"
            assert result["user_id"] == str(self.user.id)
            assert self.user.email.startswith("deleted_")
            assert self.user.email.endswith("@anonymized.local")
            assert self.user.first_name == "Deleted"
            assert self.user.last_name == "User"
            assert not self.user.is_active
            assert deactivation.is_anonymized
            assert deactivation.anonymized_at is not None
            mock_publish.assert_called_once()

    def test_anonymize_not_permanently_deactivated(self):
        AccountDeactivation.objects.create(user_id=str(self.user.id))

        with pytest.raises(ValueError, match="User must be permanently deactivated before anonymization"):
            self.service.anonymize(str(self.user.id))

    def test_anonymize_already_anonymized(self):
        deactivation = AccountDeactivation.objects.create(user_id=str(self.user.id))
        deactivation.mark_permanently_deactivated()
        deactivation.mark_anonymized()

        with pytest.raises(ValueError, match="User data is already anonymized"):
            self.service.anonymize(str(self.user.id))

    def test_anonymize_user_not_found(self):
        with pytest.raises(User.DoesNotExist):
            self.service.anonymize("999999")

    def test_anonymize_no_deactivation_record(self):
        with pytest.raises(AccountDeactivation.DoesNotExist):
            self.service.anonymize(str(self.user.id))

    def test_verify_anonymization_success(self):
        deactivation = AccountDeactivation.objects.create(user_id=str(self.user.id))
        deactivation.mark_permanently_deactivated()

        with patch.object(self.service.event_publisher, "publish_account_anonymized"):
            self.service.anonymize(str(self.user.id))

        result = self.service.verify_anonymization(str(self.user.id))

        assert result["user_id"] == str(self.user.id)
        assert result["is_anonymized"] is True
        assert result["anonymized_at"] is not None

    def test_verify_anonymization_not_anonymized(self):
        AccountDeactivation.objects.create(user_id=str(self.user.id))

        result = self.service.verify_anonymization(str(self.user.id))

        assert result["user_id"] == str(self.user.id)
        assert result["is_anonymized"] is False
        assert result["anonymized_at"] is None

    def test_publish_anonymization_event(self):
        with patch.object(self.service.event_publisher, "publish_account_anonymized") as mock_publish:
            self.service._publish_anonymization_event(str(self.user.id), "test@example.com")

            mock_publish.assert_called_once_with(
                {"user_id": str(self.user.id), "original_email": "test@example.com", "event": "account_anonymized"}
            )

    def test_anonymization_generates_unique_identifiers(self):
        deactivation = AccountDeactivation.objects.create(user_id=str(self.user.id))
        deactivation.mark_permanently_deactivated()

        user2 = User.objects.create_user(
            email="test2@example.com", password="TestPass123!", first_name="Jane", last_name="Smith"
        )
        user2.is_active = False
        user2.save()
        deactivation2 = AccountDeactivation.objects.create(user_id=str(user2.id))
        deactivation2.mark_permanently_deactivated()

        with patch.object(self.service.event_publisher, "publish_account_anonymized"):
            result1 = self.service.anonymize(str(self.user.id))
            result2 = self.service.anonymize(str(user2.id))

        self.user.refresh_from_db()
        user2.refresh_from_db()

        assert self.user.email != user2.email
        assert result1["anonymized_email"] != result2["anonymized_email"]
