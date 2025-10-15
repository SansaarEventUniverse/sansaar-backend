from unittest.mock import Mock, patch

import pytest
from django.core.exceptions import ValidationError

from application.resend_verification_service import ResendVerificationService
from domain.email_verification_token_model import EmailVerificationToken
from domain.user_model import User


@pytest.mark.django_db
class TestResendVerificationService:
    def setup_method(self):
        self.service = ResendVerificationService()

    @patch("application.resend_verification_service.EmailService")
    def test_resend_verification_success(self, mock_email_service):
        mock_email = Mock()
        mock_email_service.return_value = mock_email
        mock_email.send_verification_email.return_value = True

        user = User.objects.create_user(
            email="test@example.com", password="Test@1234", first_name="Test", last_name="User"
        )

        result = self.service.resend(user.email)

        assert result is True
        assert EmailVerificationToken.objects.filter(user=user).exists()
        mock_email.send_verification_email.assert_called_once()

    def test_resend_verification_user_not_found(self):
        with pytest.raises(ValidationError, match="User not found"):
            self.service.resend("nonexistent@example.com")

    def test_resend_verification_already_verified(self):
        user = User.objects.create_user(
            email="test@example.com", password="Test@1234", first_name="Test", last_name="User"
        )
        user.verify_email()

        with pytest.raises(ValidationError, match="Email already verified"):
            self.service.resend(user.email)
