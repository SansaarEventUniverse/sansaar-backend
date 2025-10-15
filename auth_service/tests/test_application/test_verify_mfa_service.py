import pyotp
import pytest
from django.core.exceptions import ValidationError

from application.verify_mfa_service import VerifyMFAService
from domain.mfa_secret_model import MFASecret
from domain.user_model import User


@pytest.mark.django_db
class TestVerifyMFAService:
    def setup_method(self):
        self.service = VerifyMFAService()
        self.user = User.objects.create_user(
            email="test@example.com", password="Password@123", first_name="Test", last_name="User"
        )

    def test_verify_mfa_success(self):
        secret = pyotp.random_base32()
        MFASecret.objects.create(user=self.user, secret=secret)

        # Generate real TOTP code
        totp = pyotp.TOTP(secret)
        code = totp.now()

        result = self.service.verify_mfa(self.user, code)

        assert result is True
        self.user.mfa_secret.refresh_from_db()
        assert self.user.mfa_secret.is_verified is True

    def test_verify_mfa_invalid_code(self):
        secret = pyotp.random_base32()
        MFASecret.objects.create(user=self.user, secret=secret)

        with pytest.raises(ValidationError, match="Invalid MFA code"):
            self.service.verify_mfa(self.user, "000000")

    def test_verify_mfa_no_secret(self):
        with pytest.raises(ValidationError, match="MFA not enabled"):
            self.service.verify_mfa(self.user, "123456")
