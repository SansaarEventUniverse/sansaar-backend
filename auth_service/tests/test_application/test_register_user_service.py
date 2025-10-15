import pytest
from django.core.exceptions import ValidationError

from application.register_user_service import RegisterUserService
from domain.user_model import User


@pytest.mark.django_db
class TestRegisterUserService:
    def setup_method(self):
        self.service = RegisterUserService()

    def test_register_user_success(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password": "Test@1234",
            "confirm_password": "Test@1234",
            "agree_terms": True,
        }
        user = self.service.register(data)
        assert user.email == "john@example.com"
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.is_email_verified is False

    def test_register_user_password_mismatch(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password": "Test@1234",
            "confirm_password": "Different@1234",
            "agree_terms": True,
        }
        with pytest.raises(ValidationError, match="Passwords do not match"):
            self.service.register(data)

    def test_register_user_weak_password(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password": "weak",
            "confirm_password": "weak",
            "agree_terms": True,
        }
        with pytest.raises(ValidationError, match="Password must be at least 8 characters"):
            self.service.register(data)

    def test_register_user_password_no_uppercase(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password": "test@1234",
            "confirm_password": "test@1234",
            "agree_terms": True,
        }
        with pytest.raises(ValidationError, match="Password must contain at least one uppercase letter"):
            self.service.register(data)

    def test_register_user_password_no_lowercase(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password": "TEST@1234",
            "confirm_password": "TEST@1234",
            "agree_terms": True,
        }
        with pytest.raises(ValidationError, match="Password must contain at least one lowercase letter"):
            self.service.register(data)

    def test_register_user_password_no_number(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password": "Test@abcd",
            "confirm_password": "Test@abcd",
            "agree_terms": True,
        }
        with pytest.raises(ValidationError, match="Password must contain at least one number"):
            self.service.register(data)

    def test_register_user_password_no_special_char(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password": "Test1234",
            "confirm_password": "Test1234",
            "agree_terms": True,
        }
        with pytest.raises(ValidationError, match="Password must contain at least one special character"):
            self.service.register(data)

    def test_register_user_disposable_email(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@tempmail.com",
            "password": "Test@1234",
            "confirm_password": "Test@1234",
            "agree_terms": True,
        }
        with pytest.raises(ValidationError, match="Disposable email addresses are not allowed"):
            self.service.register(data)

    def test_register_user_duplicate_email(self):
        User.objects.create_user(email="john@example.com", password="Test@1234", first_name="John", last_name="Doe")
        data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "john@example.com",
            "password": "Test@1234",
            "confirm_password": "Test@1234",
            "agree_terms": True,
        }
        with pytest.raises(ValidationError, match="Email already registered"):
            self.service.register(data)

    def test_register_user_terms_not_agreed(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password": "Test@1234",
            "confirm_password": "Test@1234",
            "agree_terms": False,
        }
        with pytest.raises(ValidationError, match="You must agree to the terms and conditions"):
            self.service.register(data)
