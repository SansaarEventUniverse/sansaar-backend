import pytest
from rest_framework.test import APIClient

from domain.login_attempt_model import LoginAttempt
from domain.user_model import User


@pytest.mark.django_db
class TestAccountLockoutAPI:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@example.com",
            password="Password@123",
            first_name="Test",
            last_name="User",
            is_email_verified=True,
        )

    def test_lockout_returns_429_status(self):
        # Create 5 failed attempts
        for _ in range(5):
            LoginAttempt.objects.create(user=self.user, ip_address="127.0.0.1", success=False)

        # Try to login
        response = self.client.post("/api/auth/login/", {"email": "test@example.com", "password": "Password@123"})

        assert response.status_code == 429
        assert "locked" in response.json()["error"].lower()

    def test_lockout_message_includes_info(self):
        # Create 5 failed attempts
        for _ in range(5):
            LoginAttempt.objects.create(user=self.user, ip_address="127.0.0.1", success=False)

        response = self.client.post("/api/auth/login/", {"email": "test@example.com", "password": "Password@123"})

        assert "too many failed" in response.json()["error"].lower()

    def test_failed_login_returns_401(self):
        response = self.client.post("/api/auth/login/", {"email": "test@example.com", "password": "WrongPassword"})

        assert response.status_code == 401

    def test_successful_login_after_failed_attempts(self):
        # Create 2 failed attempts
        for _ in range(2):
            self.client.post("/api/auth/login/", {"email": "test@example.com", "password": "WrongPassword"})

        # Successful login
        response = self.client.post("/api/auth/login/", {"email": "test@example.com", "password": "Password@123"})

        assert response.status_code == 200
        assert "access_token" in response.json()
