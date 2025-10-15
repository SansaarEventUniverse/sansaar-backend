from datetime import timedelta

import pytest
from django.utils import timezone

from domain.refresh_token_model import RefreshToken
from domain.user_model import User


@pytest.mark.django_db
class TestRefreshToken:
    def test_create_refresh_token(self):
        user = User.objects.create_user(
            email="test@example.com", password="Test@1234", first_name="Test", last_name="User"
        )
        token = RefreshToken.objects.create(user=user)

        assert token.user == user
        assert len(token.token) == 64
        assert token.expires_at > timezone.now()
        assert token.is_blacklisted is False

    def test_token_expires_in_7_days(self):
        user = User.objects.create_user(
            email="test@example.com", password="Test@1234", first_name="Test", last_name="User"
        )
        token = RefreshToken.objects.create(user=user)

        expected_expiry = timezone.now() + timedelta(days=7)
        assert abs((token.expires_at - expected_expiry).total_seconds()) < 5

    def test_is_expired_method(self):
        user = User.objects.create_user(
            email="test@example.com", password="Test@1234", first_name="Test", last_name="User"
        )
        token = RefreshToken.objects.create(user=user)

        assert token.is_expired() is False

        token.expires_at = timezone.now() - timedelta(hours=1)
        token.save()
        assert token.is_expired() is True

    def test_blacklist_method(self):
        user = User.objects.create_user(
            email="test@example.com", password="Test@1234", first_name="Test", last_name="User"
        )
        token = RefreshToken.objects.create(user=user)

        assert token.is_blacklisted is False
        token.blacklist()
        assert token.is_blacklisted is True

    def test_token_str_representation(self):
        user = User.objects.create_user(
            email="test@example.com", password="Test@1234", first_name="Test", last_name="User"
        )
        token = RefreshToken.objects.create(user=user)

        assert str(token) == f"RefreshToken for {user.email}"
