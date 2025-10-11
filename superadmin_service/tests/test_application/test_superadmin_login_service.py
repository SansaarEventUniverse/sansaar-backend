from unittest.mock import Mock

import bcrypt
import pyotp
import pytest
from django.core.exceptions import ValidationError

from application.superadmin_login_service import SuperAdminLoginService
from domain.superadmin_model import SuperAdmin


@pytest.mark.django_db
class TestSuperAdminLoginService:
    def test_login_success(self):
        secret = pyotp.random_base32()
        password = "password123"
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        SuperAdmin.objects.create(email="admin@example.com", password_hash=hashed, mfa_secret=secret)

        ip_service = Mock()
        ip_service.is_whitelisted.return_value = True

        jwt_service = Mock()
        jwt_service.generate_token.return_value = "test_token"

        service = SuperAdminLoginService(ip_service, jwt_service)

        totp = pyotp.TOTP(secret)
        token = totp.now()

        result = service.login("admin@example.com", password, token, "192.168.1.1")

        assert result["token"] == "test_token"
        assert result["email"] == "admin@example.com"
        ip_service.is_whitelisted.assert_called_once_with("192.168.1.1")

    def test_login_ip_not_whitelisted(self):
        ip_service = Mock()
        ip_service.is_whitelisted.return_value = False

        jwt_service = Mock()
        service = SuperAdminLoginService(ip_service, jwt_service)

        with pytest.raises(ValidationError, match="IP address not whitelisted"):
            service.login("admin@example.com", "password", "123456", "192.168.1.1")

    def test_login_invalid_email(self):
        ip_service = Mock()
        ip_service.is_whitelisted.return_value = True

        jwt_service = Mock()
        service = SuperAdminLoginService(ip_service, jwt_service)

        with pytest.raises(ValidationError, match="Invalid credentials"):
            service.login("nonexistent@example.com", "password", "123456", "192.168.1.1")

    def test_login_invalid_password(self):
        secret = pyotp.random_base32()
        hashed = bcrypt.hashpw(b"password123", bcrypt.gensalt()).decode()

        SuperAdmin.objects.create(email="admin@example.com", password_hash=hashed, mfa_secret=secret)

        ip_service = Mock()
        ip_service.is_whitelisted.return_value = True

        jwt_service = Mock()
        service = SuperAdminLoginService(ip_service, jwt_service)

        with pytest.raises(ValidationError, match="Invalid credentials"):
            service.login("admin@example.com", "wrongpassword", "123456", "192.168.1.1")

    def test_login_invalid_mfa(self):
        secret = pyotp.random_base32()
        password = "password123"
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        SuperAdmin.objects.create(email="admin@example.com", password_hash=hashed, mfa_secret=secret)

        ip_service = Mock()
        ip_service.is_whitelisted.return_value = True

        jwt_service = Mock()
        service = SuperAdminLoginService(ip_service, jwt_service)

        with pytest.raises(ValidationError, match="Invalid MFA token"):
            service.login("admin@example.com", password, "000000", "192.168.1.1")

    def test_login_inactive_admin(self):
        secret = pyotp.random_base32()
        password = "password123"
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        SuperAdmin.objects.create(email="admin@example.com", password_hash=hashed, mfa_secret=secret, is_active=False)

        ip_service = Mock()
        ip_service.is_whitelisted.return_value = True

        jwt_service = Mock()
        service = SuperAdminLoginService(ip_service, jwt_service)

        totp = pyotp.TOTP(secret)
        token = totp.now()

        with pytest.raises(ValidationError, match="SuperAdmin account is inactive"):
            service.login("admin@example.com", password, token, "192.168.1.1")
