import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestDisposableEmailAPI:
    def setup_method(self):
        self.client = APIClient()

    def test_register_with_disposable_email_blocked(self):
        response = self.client.post(
            "/api/auth/register/",
            {
                "email": "test@tempmail.com",
                "password": "Password@123",
                "confirm_password": "Password@123",
                "first_name": "Test",
                "last_name": "User",
                "agree_terms": True,
            },
        )

        assert response.status_code == 400
        assert "disposable" in str(response.json()).lower()

    def test_register_with_valid_email_allowed(self):
        response = self.client.post(
            "/api/auth/register/",
            {
                "email": "test@gmail.com",
                "password": "Password@123",
                "confirm_password": "Password@123",
                "first_name": "Test",
                "last_name": "User",
                "agree_terms": True,
            },
        )

        assert response.status_code == 201
        assert response.json()["user"]["email"] == "test@gmail.com"

    def test_multiple_disposable_domains_blocked(self):
        disposable_emails = ["user@guerrillamail.com", "test@10minutemail.com", "admin@mailinator.com"]

        for email in disposable_emails:
            response = self.client.post(
                "/api/auth/register/",
                {
                    "email": email,
                    "password": "Password@123",
                    "confirm_password": "Password@123",
                    "first_name": "Test",
                    "last_name": "User",
                    "agree_terms": True,
                },
            )

            assert response.status_code == 400
            assert "disposable" in str(response.json()).lower()
