from datetime import timedelta

import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone

from application.verify_email_service import VerifyEmailService
from domain.email_verification_token_model import EmailVerificationToken
from domain.user_model import User


@pytest.mark.django_db
class TestVerifyEmailService:
    def setup_method(self):
        self.service = VerifyEmailService()

    def test_verify_email_success(self):
        user = User.objects.create_user(
            email='test@example.com',
            password='Test@1234',
            first_name='Test',
            last_name='User'
        )
        token = EmailVerificationToken.objects.create(user=user)

        result = self.service.verify(token.token)

        assert result is True
        user.refresh_from_db()
        assert user.is_email_verified is True

    def test_verify_email_invalid_token(self):
        with pytest.raises(ValidationError, match='Invalid or expired token'):
            self.service.verify('invalid-token')

    def test_verify_email_expired_token(self):
        user = User.objects.create_user(
            email='test@example.com',
            password='Test@1234',
            first_name='Test',
            last_name='User'
        )
        token = EmailVerificationToken.objects.create(user=user)
        token.expires_at = timezone.now() - timedelta(hours=1)
        token.save()

        with pytest.raises(ValidationError, match='Invalid or expired token'):
            self.service.verify(token.token)

    def test_verify_email_already_verified(self):
        user = User.objects.create_user(
            email='test@example.com',
            password='Test@1234',
            first_name='Test',
            last_name='User'
        )
        user.verify_email()
        token = EmailVerificationToken.objects.create(user=user)

        with pytest.raises(ValidationError, match='Email already verified'):
            self.service.verify(token.token)
