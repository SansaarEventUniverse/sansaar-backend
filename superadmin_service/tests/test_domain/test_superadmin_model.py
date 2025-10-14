import pyotp
import pytest
from django.core.exceptions import ValidationError

from domain.superadmin_model import SuperAdmin


@pytest.mark.django_db
class TestSuperAdminModel:
    def test_create_superadmin(self):
        admin = SuperAdmin.objects.create(
            email="admin@example.com", password_hash="hashed_password", mfa_secret=pyotp.random_base32()
        )
        assert admin.email == "admin@example.com"
        assert admin.is_active is True
        assert admin.mfa_secret is not None

    def test_generate_mfa_secret(self):
        admin = SuperAdmin.objects.create(email="admin@example.com", password_hash="hashed_password", mfa_secret="")
        secret = admin.generate_mfa_secret()
        assert len(secret) == 32
        assert admin.mfa_secret == secret

    def test_verify_mfa_valid_token(self):
        secret = pyotp.random_base32()
        admin = SuperAdmin.objects.create(email="admin@example.com", password_hash="hashed_password", mfa_secret=secret)
        totp = pyotp.TOTP(secret)
        token = totp.now()
        assert admin.verify_mfa(token) is True

    def test_verify_mfa_invalid_token(self):
        secret = pyotp.random_base32()
        admin = SuperAdmin.objects.create(email="admin@example.com", password_hash="hashed_password", mfa_secret=secret)
        assert admin.verify_mfa("000000") is False

    def test_verify_mfa_no_secret(self):
        admin = SuperAdmin.objects.create(email="admin@example.com", password_hash="hashed_password", mfa_secret="")
        with pytest.raises(ValidationError, match="MFA not configured"):
            admin.verify_mfa("123456")

    def test_get_mfa_uri(self):
        secret = pyotp.random_base32()
        admin = SuperAdmin.objects.create(email="admin@example.com", password_hash="hashed_password", mfa_secret=secret)
        uri = admin.get_mfa_uri()
        assert "otpauth://totp/" in uri
        assert "admin%40example.com" in uri or "admin@example.com" in uri
        assert "SansaarEventUniverse" in uri

    def test_get_mfa_uri_no_secret(self):
        admin = SuperAdmin.objects.create(email="admin@example.com", password_hash="hashed_password", mfa_secret="")
        with pytest.raises(ValidationError, match="MFA not configured"):
            admin.get_mfa_uri()

    def test_validate_active_success(self):
        admin = SuperAdmin.objects.create(
            email="admin@example.com", password_hash="hashed_password", mfa_secret=pyotp.random_base32(), is_active=True
        )
        admin.validate_active()

    def test_validate_active_inactive(self):
        admin = SuperAdmin.objects.create(
            email="admin@example.com",
            password_hash="hashed_password",
            mfa_secret=pyotp.random_base32(),
            is_active=False,
        )
        with pytest.raises(ValidationError, match="SuperAdmin account is inactive"):
            admin.validate_active()

    def test_unique_email(self):
        SuperAdmin.objects.create(email="admin@example.com", password_hash="hashed_password", mfa_secret="secret")
        with pytest.raises(Exception):
            SuperAdmin.objects.create(email="admin@example.com", password_hash="hashed_password2", mfa_secret="secret2")
