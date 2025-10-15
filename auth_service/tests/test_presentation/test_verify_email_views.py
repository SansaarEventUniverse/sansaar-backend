import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from domain.email_verification_token_model import EmailVerificationToken
from domain.user_model import User


@pytest.mark.django_db
class TestVerifyEmailView:
    def setup_method(self):
        self.client = APIClient()

    def test_verify_email_success(self):
        user = User.objects.create_user(
            email="test@example.com", password="Test@1234", first_name="Test", last_name="User"
        )
        token = EmailVerificationToken.objects.create(user=user)

        url = reverse("verify_email", kwargs={"token": token.token})
        response = self.client.get(url)

        assert response.status_code == 200
        assert response.data["message"] == "Email verified successfully"
        user.refresh_from_db()
        assert user.is_email_verified is True

    def test_verify_email_invalid_token(self):
        url = reverse("verify_email", kwargs={"token": "invalid-token"})
        response = self.client.get(url)

        assert response.status_code == 400
        assert "error" in response.data


@pytest.mark.django_db
class TestResendVerificationView:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse("resend_verification")

    def test_resend_verification_success(self):
        user = User.objects.create_user(
            email="test@example.com", password="Test@1234", first_name="Test", last_name="User"
        )

        data = {"email": user.email}
        response = self.client.post(self.url, data, format="json")

        assert response.status_code == 200
        assert response.data["message"] == "Verification email sent successfully"

    def test_resend_verification_user_not_found(self):
        data = {"email": "nonexistent@example.com"}
        response = self.client.post(self.url, data, format="json")

        assert response.status_code == 400
        assert "error" in response.data

    def test_resend_verification_missing_email(self):
        response = self.client.post(self.url, {}, format="json")

        assert response.status_code == 400
        assert "email" in response.data
