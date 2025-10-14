import bcrypt
import pyotp
import pytest
from django.test import Client

from domain.ip_whitelist_model import IPWhitelist
from domain.superadmin_model import SuperAdmin


@pytest.mark.django_db
class TestSuperAdminAuthAPI:
    def test_login_success(self):
        secret = pyotp.random_base32()
        password = "password123"
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        SuperAdmin.objects.create(email="admin@example.com", password_hash=hashed, mfa_secret=secret)
        IPWhitelist.objects.create(ip_address="127.0.0.1", is_active=True)

        client = Client()
        totp = pyotp.TOTP(secret)
        token = totp.now()

        response = client.post(
            "/api/superadmin/auth/login/",
            {"email": "admin@example.com", "password": password, "mfa_token": token},
            content_type="application/json",
        )

        assert response.status_code == 200
        assert "token" in response.json()
        assert response.json()["email"] == "admin@example.com"

    def test_login_invalid_credentials(self):
        IPWhitelist.objects.create(ip_address="127.0.0.1", is_active=True)

        client = Client()
        response = client.post(
            "/api/superadmin/auth/login/",
            {"email": "admin@example.com", "password": "wrong", "mfa_token": "123456"},
            content_type="application/json",
        )

        assert response.status_code == 401
        assert "error" in response.json()

    def test_login_ip_not_whitelisted(self):
        secret = pyotp.random_base32()
        password = "password123"
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        SuperAdmin.objects.create(email="admin@example.com", password_hash=hashed, mfa_secret=secret)

        client = Client()
        totp = pyotp.TOTP(secret)
        token = totp.now()

        response = client.post(
            "/api/superadmin/auth/login/",
            {"email": "admin@example.com", "password": password, "mfa_token": token},
            content_type="application/json",
        )

        assert response.status_code == 401
        assert "IP address not whitelisted" in response.json()["error"]

    def test_login_invalid_mfa(self):
        secret = pyotp.random_base32()
        password = "password123"
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        SuperAdmin.objects.create(email="admin@example.com", password_hash=hashed, mfa_secret=secret)
        IPWhitelist.objects.create(ip_address="127.0.0.1", is_active=True)

        client = Client()
        response = client.post(
            "/api/superadmin/auth/login/",
            {"email": "admin@example.com", "password": password, "mfa_token": "000000"},
            content_type="application/json",
        )

        assert response.status_code == 401
        assert "Invalid MFA token" in response.json()["error"]

    def test_logout_success(self):
        secret = pyotp.random_base32()
        password = "password123"
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        SuperAdmin.objects.create(email="admin@example.com", password_hash=hashed, mfa_secret=secret)
        IPWhitelist.objects.create(ip_address="127.0.0.1", is_active=True)

        client = Client()
        totp = pyotp.TOTP(secret)
        token = totp.now()

        login_response = client.post(
            "/api/superadmin/auth/login/",
            {"email": "admin@example.com", "password": password, "mfa_token": token},
            content_type="application/json",
        )

        jwt_token = login_response.json()["token"]

        logout_response = client.post("/api/superadmin/auth/logout/", HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        assert logout_response.status_code == 200
        assert logout_response.json()["message"] == "Logged out successfully"

    def test_logout_no_token(self):
        client = Client()
        response = client.post("/api/superadmin/auth/logout/")

        assert response.status_code == 401
        assert "Authorization header required" in response.json()["error"]
