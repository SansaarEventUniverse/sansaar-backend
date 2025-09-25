import pytest

from domain.user_profile_model import UserProfile
from infrastructure.messaging.user_registered_event_handler import UserRegisteredEventHandler


@pytest.mark.django_db
class TestUserRegisteredEventHandler:
    def setup_method(self):
        self.handler = UserRegisteredEventHandler()

    def test_handle_user_registered_event(self):
        event_data = {"user_id": "123", "email": "test@example.com", "first_name": "John", "last_name": "Doe"}

        self.handler.handle(event_data)

        profile = UserProfile.objects.get(user_id="123")
        assert profile.email == "test@example.com"
        assert profile.first_name == "John"
        assert profile.last_name == "Doe"

    def test_handle_duplicate_user_registered_event(self):
        UserProfile.objects.create(user_id="123", email="test@example.com", first_name="John", last_name="Doe")

        event_data = {"user_id": "123", "email": "test@example.com", "first_name": "John", "last_name": "Doe"}

        # Should not raise error, just skip
        self.handler.handle(event_data)

        assert UserProfile.objects.filter(user_id="123").count() == 1
