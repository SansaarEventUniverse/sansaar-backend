import pytest
from django.contrib.auth.hashers import check_password

from domain.user_model import User


@pytest.mark.django_db
class TestUserModel:
    def test_create_user_with_valid_data(self):
        user = User.objects.create_user(
            email="test@example.com", password="Test@1234", first_name="Test", last_name="User"
        )
        assert user.email == "test@example.com"
        assert user.first_name == "Test"
        assert user.last_name == "User"
        assert user.is_email_verified is False
        assert user.is_active is True
        assert check_password("Test@1234", user.password)

    def test_create_user_email_normalized(self):
        user = User.objects.create_user(
            email="Test@Example.COM", password="Test@1234", first_name="Test", last_name="User"
        )
        assert user.email == "Test@example.com"

    def test_create_user_without_email_raises_error(self):
        with pytest.raises(ValueError):
            User.objects.create_user(email="", password="Test@1234")

    def test_verify_email_method(self):
        user = User.objects.create_user(
            email="test@example.com", password="Test@1234", first_name="Test", last_name="User"
        )
        assert user.is_email_verified is False
        user.verify_email()
        assert user.is_email_verified is True

    def test_activate_method(self):
        user = User.objects.create_user(
            email="test@example.com", password="Test@1234", first_name="Test", last_name="User"
        )
        user.is_active = False
        user.save()
        user.activate()
        assert user.is_active is True

    def test_deactivate_method(self):
        user = User.objects.create_user(
            email="test@example.com", password="Test@1234", first_name="Test", last_name="User"
        )
        user.deactivate()
        assert user.is_active is False

    def test_email_unique_constraint(self):
        User.objects.create_user(email="test@example.com", password="Test@1234", first_name="Test", last_name="User")
        with pytest.raises(Exception):
            User.objects.create_user(
                email="test@example.com", password="Test@5678", first_name="Another", last_name="User"
            )

    def test_user_str_representation(self):
        user = User.objects.create_user(
            email="test@example.com", password="Test@1234", first_name="Test", last_name="User"
        )
        assert str(user) == "test@example.com"
