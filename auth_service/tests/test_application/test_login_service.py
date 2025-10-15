import pytest
from django.core.exceptions import ValidationError

from application.login_service import LoginService
from domain.user_model import User


@pytest.mark.django_db
class TestLoginService:
    def setup_method(self):
        self.service = LoginService()
        self.user = User.objects.create_user(
            email="test@example.com", password="Test@1234", first_name="Test", last_name="User"
        )
        self.user.verify_email()

    def test_login_success(self):
        result = self.service.login("test@example.com", "Test@1234")

        assert "access_token" in result
        assert "refresh_token" in result
        assert "user" in result
        assert result["user"]["email"] == "test@example.com"

    def test_login_invalid_email(self):
        with pytest.raises(ValidationError, match="Invalid email or password"):
            self.service.login("wrong@example.com", "Test@1234")

    def test_login_invalid_password(self):
        with pytest.raises(ValidationError, match="Invalid email or password"):
            self.service.login("test@example.com", "WrongPassword")

    def test_login_unverified_email(self):
        User.objects.create_user(
            email="unverified@example.com", password="Test@1234", first_name="Unverified", last_name="User"
        )

        with pytest.raises(ValidationError, match="Email not verified"):
            self.service.login("unverified@example.com", "Test@1234")

    def test_login_inactive_user(self):
        self.user.deactivate()

        with pytest.raises(ValidationError, match="Account is inactive"):
            self.service.login("test@example.com", "Test@1234")
