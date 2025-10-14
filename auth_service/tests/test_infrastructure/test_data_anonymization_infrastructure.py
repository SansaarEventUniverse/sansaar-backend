import uuid
from unittest.mock import MagicMock, patch

import pytest

from application.anonymize_account_service import AnonymizeUserDataService
from domain.models import AccountDeactivation, User
from infrastructure.repositories.user_repository import UserRepository


@pytest.mark.django_db
class TestDataAnonymizationInfrastructure:
    def setup_method(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="TestPass123!", first_name="John", last_name="Doe"
        )
        self.user.is_active = False
        self.user.save()

    def test_user_repository_anonymize_user_data(self):
        anonymized_email = f"deleted_{uuid.uuid4().hex[:8]}@anonymized.local"

        result = UserRepository.anonymize_user_data(str(self.user.id), anonymized_email)

        assert result.email == anonymized_email
        assert result.first_name == "Deleted"
        assert result.last_name == "User"
        assert not result.is_active

    def test_user_repository_get_user_by_id(self):
        user = UserRepository.get_user_by_id(str(self.user.id))
        assert user.id == self.user.id
        assert user.email == "test@example.com"

    def test_user_repository_is_user_anonymized(self):
        assert not UserRepository.is_user_anonymized(str(self.user.id))

        anonymized_email = f"deleted_{uuid.uuid4().hex[:8]}@anonymized.local"
        UserRepository.anonymize_user_data(str(self.user.id), anonymized_email)

        assert UserRepository.is_user_anonymized(str(self.user.id))

    def test_event_publisher_publish_account_anonymized(self):
        service = AnonymizeUserDataService()

        with patch("pika.BlockingConnection") as mock_connection:
            mock_channel = MagicMock()
            mock_connection.return_value.channel.return_value = mock_channel

            result = service.event_publisher.publish_account_anonymized(
                {"user_id": str(self.user.id), "original_email": "test@example.com", "event": "account_anonymized"}
            )

            assert result is True
            mock_channel.exchange_declare.assert_called_once_with(
                exchange="auth_events", exchange_type="topic", durable=True
            )
            mock_channel.basic_publish.assert_called_once()

    def test_cross_service_anonymization_coordination(self):
        deactivation = AccountDeactivation.objects.create(user_id=str(self.user.id))
        deactivation.mark_permanently_deactivated()

        service = AnonymizeUserDataService()

        with patch.object(service.event_publisher, "publish_account_anonymized") as mock_publish:
            result = service.anonymize(str(self.user.id))

            # Verify auth_service anonymization
            self.user.refresh_from_db()
            assert self.user.email.startswith("deleted_")
            assert self.user.email.endswith("@anonymized.local")

            # Verify event published for user_org_service
            mock_publish.assert_called_once()
            call_args = mock_publish.call_args[0][0]
            assert call_args["user_id"] == str(self.user.id)
            assert call_args["original_email"] == "test@example.com"
            assert call_args["event"] == "account_anonymized"

    def test_anonymization_verification_integration(self):
        deactivation = AccountDeactivation.objects.create(user_id=str(self.user.id))
        deactivation.mark_permanently_deactivated()

        service = AnonymizeUserDataService()

        with patch.object(service.event_publisher, "publish_account_anonymized"):
            service.anonymize(str(self.user.id))

        # Verify using repository
        assert UserRepository.is_user_anonymized(str(self.user.id))

        # Verify using service
        verification = service.verify_anonymization(str(self.user.id))
        assert verification["is_anonymized"] is True

    def test_event_publishing_failure_handling(self):
        deactivation = AccountDeactivation.objects.create(user_id=str(self.user.id))
        deactivation.mark_permanently_deactivated()

        service = AnonymizeUserDataService()

        with patch("pika.BlockingConnection", side_effect=Exception("Connection failed")):
            # Anonymization should still complete even if event publishing fails
            result = service.anonymize(str(self.user.id))

            self.user.refresh_from_db()
            assert result["message"] == "Account anonymized successfully"
            assert self.user.email.startswith("deleted_")
