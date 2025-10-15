import pytest
from rest_framework.test import APIClient

from domain.session_model import Session
from domain.user_model import User


@pytest.mark.django_db
class TestSessionAPI:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@example.com",
            password="Password@123",
            first_name="Test",
            last_name="User",
            is_email_verified=True,
        )

    def test_list_sessions(self):
        # Create sessions
        for i in range(3):
            Session.objects.create(user=self.user, ip_address=f"192.168.1.{i}", user_agent="Mozilla/5.0")

        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/auth/sessions/")

        assert response.status_code == 200
        assert len(response.json()) == 3

    def test_list_sessions_unauthenticated(self):
        response = self.client.get("/api/auth/sessions/")
        assert response.status_code == 403

    def test_revoke_session(self):
        session = Session.objects.create(user=self.user, ip_address="192.168.1.1", user_agent="Mozilla/5.0")

        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/api/auth/sessions/{session.id}/")

        assert response.status_code == 200
        session.refresh_from_db()
        assert session.is_active is False

    def test_revoke_session_not_owned(self):
        other_user = User.objects.create_user(
            email="other@example.com", password="Password@123", first_name="Other", last_name="User"
        )
        session = Session.objects.create(user=other_user, ip_address="192.168.1.1", user_agent="Mozilla/5.0")

        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/api/auth/sessions/{session.id}/")

        assert response.status_code == 404

    def test_revoke_all_sessions(self):
        # Create sessions
        for i in range(3):
            Session.objects.create(user=self.user, ip_address=f"192.168.1.{i}", user_agent="Mozilla/5.0")

        self.client.force_authenticate(user=self.user)
        response = self.client.delete("/api/auth/sessions/all/")

        assert response.status_code == 200
        assert response.json()["revoked_count"] == 3
