import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone

from application.logout_service import LogoutService
from domain.refresh_token_model import RefreshToken
from domain.user_model import User


@pytest.mark.django_db
class TestLogoutService:
    def setup_method(self):
        self.service = LogoutService()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='Password@123',
            first_name='Test',
            last_name='User',
            is_email_verified=True
        )

    def test_logout_success(self):
        token = RefreshToken.objects.create(
            user=self.user,
            token='test_refresh_token',
            expires_at=timezone.now() + timezone.timedelta(days=7)
        )

        self.service.logout('test_refresh_token')

        token.refresh_from_db()
        assert token.is_blacklisted is True

    def test_logout_invalid_token(self):
        with pytest.raises(ValidationError, match='Invalid refresh token'):
            self.service.logout('nonexistent_token')

    def test_logout_already_blacklisted(self):
        RefreshToken.objects.create(
            user=self.user,
            token='test_refresh_token',
            expires_at=timezone.now() + timezone.timedelta(days=7),
            is_blacklisted=True
        )

        with pytest.raises(ValidationError, match='Token already blacklisted'):
            self.service.logout('test_refresh_token')

    def test_logout_expired_token(self):
        RefreshToken.objects.create(
            user=self.user,
            token='test_refresh_token',
            expires_at=timezone.now() - timezone.timedelta(days=1)
        )

        with pytest.raises(ValidationError, match='Token has expired'):
            self.service.logout('test_refresh_token')
