import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from domain.user_model import User


@pytest.mark.django_db
class TestRegisterView:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse("register")

    def test_register_user_success(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password": "Test@1234",
            "confirm_password": "Test@1234",
            "agree_terms": True,
        }
        response = self.client.post(self.url, data, format="json")

        assert response.status_code == 201
        assert response.data["message"] == "User registered successfully"
        assert "user" in response.data
        assert response.data["user"]["email"] == "john@example.com"
        assert User.objects.filter(email="john@example.com").exists()

    def test_register_user_missing_fields(self):
        data = {"email": "john@example.com", "password": "Test@1234"}
        response = self.client.post(self.url, data, format="json")

        assert response.status_code == 400
        assert "first_name" in response.data

    def test_register_user_invalid_email(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "invalid-email",
            "password": "Test@1234",
            "confirm_password": "Test@1234",
            "agree_terms": True,
        }
        response = self.client.post(self.url, data, format="json")

        assert response.status_code == 400
        assert "email" in response.data

    def test_register_user_password_mismatch(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password": "Test@1234",
            "confirm_password": "Different@1234",
            "agree_terms": True,
        }
        response = self.client.post(self.url, data, format="json")

        assert response.status_code == 400
        assert "non_field_errors" in response.data

    def test_register_user_weak_password(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password": "weak",
            "confirm_password": "weak",
            "agree_terms": True,
        }
        response = self.client.post(self.url, data, format="json")

        assert response.status_code == 400

    def test_register_user_duplicate_email(self):
        User.objects.create_user(email="john@example.com", password="Test@1234", first_name="John", last_name="Doe")
        data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "john@example.com",
            "password": "Test@1234",
            "confirm_password": "Test@1234",
            "agree_terms": True,
        }
        response = self.client.post(self.url, data, format="json")

        assert response.status_code == 400
