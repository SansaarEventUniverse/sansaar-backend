import pytest
from django.core.exceptions import ValidationError

from application.register_user_service import RegisterUserService


@pytest.mark.django_db
class TestDisposableEmailBlocking:
    def test_register_with_disposable_email(self):
        service = RegisterUserService()

        with pytest.raises(ValidationError) as exc_info:
            service.register(
                {
                    "email": "test@tempmail.com",
                    "password": "Password@123",
                    "confirm_password": "Password@123",
                    "first_name": "Test",
                    "last_name": "User",
                    "agree_terms": True,
                }
            )

        assert "disposable" in str(exc_info.value).lower()

    def test_register_with_valid_email(self):
        service = RegisterUserService()

        user = service.register(
            {
                "email": "test@gmail.com",
                "password": "Password@123",
                "confirm_password": "Password@123",
                "first_name": "Test",
                "last_name": "User",
                "agree_terms": True,
            }
        )

        assert user.email == "test@gmail.com"

    def test_register_with_multiple_disposable_domains(self):
        service = RegisterUserService()
        disposable_emails = ["user@guerrillamail.com", "test@10minutemail.com", "admin@mailinator.com"]

        for email in disposable_emails:
            with pytest.raises(ValidationError) as exc_info:
                service.register(
                    {
                        "email": email,
                        "password": "Password@123",
                        "confirm_password": "Password@123",
                        "first_name": "Test",
                        "last_name": "User",
                        "agree_terms": True,
                    }
                )
            assert "disposable" in str(exc_info.value).lower()
