import pytest
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from domain.refresh_token_model import RefreshToken
from domain.user_model import User


@pytest.mark.django_db
class TestLogoutView:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@example.com",
            password="Password@123",
            first_name="Test",
            last_name="User",
            is_email_verified=True,
        )

    def test_logout_success(self):
        token = RefreshToken.objects.create(
            user=self.user, token="test_refresh_token", expires_at=timezone.now() + timezone.timedelta(days=7)
        )

        response = self.client.post("/api/auth/logout/", {"refresh_token": "test_refresh_token"})

        assert response.status_code == status.HTTP_200_OK
        assert response.data["message"] == "Logged out successfully"

        token.refresh_from_db()
        assert token.is_blacklisted is True

    def test_logout_invalid_token(self):
        response = self.client.post("/api/auth/logout/", {"refresh_token": "invalid_token"})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid refresh token" in str(response.data)

    def test_logout_missing_token(self):
        response = self.client.post("/api/auth/logout/", {})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_logout_already_blacklisted(self):
        RefreshToken.objects.create(
            user=self.user,
            token="test_refresh_token",
            expires_at=timezone.now() + timezone.timedelta(days=7),
            is_blacklisted=True,
        )

        response = self.client.post("/api/auth/logout/", {"refresh_token": "test_refresh_token"})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Token already blacklisted" in str(response.data)
