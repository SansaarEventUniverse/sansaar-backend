import pyotp
import pytest
from rest_framework import status
from rest_framework.test import APIClient

from domain.mfa_secret_model import MFASecret
from domain.user_model import User


@pytest.mark.django_db
class TestMFAViews:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@example.com",
            password="Password@123",
            first_name="Test",
            last_name="User",
            is_email_verified=True,
        )

    def test_enable_mfa(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post("/api/auth/mfa/enable/")

        assert response.status_code == status.HTTP_200_OK
        assert "secret" in response.data
        assert "qr_code_data" in response.data
        assert "backup_codes" in response.data
        assert len(response.data["backup_codes"]) == 10

    def test_verify_mfa(self):
        secret = pyotp.random_base32()
        MFASecret.objects.create(user=self.user, secret=secret)

        totp = pyotp.TOTP(secret)
        code = totp.now()

        self.client.force_authenticate(user=self.user)
        response = self.client.post("/api/auth/mfa/verify/", {"code": code})

        assert response.status_code == status.HTTP_200_OK
        assert response.data["message"] == "MFA verified successfully"

    def test_disable_mfa(self):
        MFASecret.objects.create(user=self.user, secret="JBSWY3DPEHPK3PXP", is_verified=True)

        self.client.force_authenticate(user=self.user)
        response = self.client.post("/api/auth/mfa/disable/")

        assert response.status_code == status.HTTP_200_OK
        assert not MFASecret.objects.filter(user=self.user).exists()

    def test_login_with_mfa_required(self):
        secret = pyotp.random_base32()
        MFASecret.objects.create(user=self.user, secret=secret, is_verified=True)

        response = self.client.post("/api/auth/login/", {"email": "test@example.com", "password": "Password@123"})

        assert response.status_code == status.HTTP_200_OK
        assert "mfa_required" in response.data
        assert response.data["mfa_required"] is True

    def test_login_with_mfa_code(self):
        secret = pyotp.random_base32()
        MFASecret.objects.create(user=self.user, secret=secret, is_verified=True)

        totp = pyotp.TOTP(secret)
        code = totp.now()

        response = self.client.post(
            "/api/auth/login/", {"email": "test@example.com", "password": "Password@123", "mfa_code": code}
        )

        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.data
