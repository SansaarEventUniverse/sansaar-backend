from datetime import timedelta

import pytest
from django.utils import timezone

from domain.password_reset_token_model import PasswordResetToken
from domain.user_model import User


@pytest.mark.django_db
class TestPasswordResetToken:
    def test_create_token(self):
        user = User.objects.create_user(
            email="test@example.com", password="Test@1234", first_name="Test", last_name="User"
        )
        token = PasswordResetToken.objects.create(user=user)

        assert token.user == user
        assert len(token.token) == 64
        assert token.expires_at > timezone.now()

    def test_token_expires_in_1_hour(self):
        user = User.objects.create_user(
            email="test@example.com", password="Test@1234", first_name="Test", last_name="User"
        )
        token = PasswordResetToken.objects.create(user=user)

        expected_expiry = timezone.now() + timedelta(hours=1)
        assert abs((token.expires_at - expected_expiry).total_seconds()) < 5

    def test_is_expired_method(self):
        user = User.objects.create_user(
            email="test@example.com", password="Test@1234", first_name="Test", last_name="User"
        )
        token = PasswordResetToken.objects.create(user=user)

        assert token.is_expired() is False

        token.expires_at = timezone.now() - timedelta(hours=1)
        token.save()
        assert token.is_expired() is True

    def test_token_str_representation(self):
        user = User.objects.create_user(
            email="test@example.com", password="Test@1234", first_name="Test", last_name="User"
        )
        token = PasswordResetToken.objects.create(user=user)

        assert str(token) == f"PasswordResetToken for {user.email}"
