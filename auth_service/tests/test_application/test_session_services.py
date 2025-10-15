import pytest

from application.create_session_service import CreateSessionService
from application.list_sessions_service import ListSessionsService
from application.revoke_all_sessions_service import RevokeAllSessionsService
from application.revoke_session_service import RevokeSessionService
from domain.session_model import Session
from domain.user_model import User


@pytest.mark.django_db
class TestSessionServices:
    def setup_method(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="Password@123", first_name="Test", last_name="User"
        )

    def test_create_session(self):
        service = CreateSessionService()
        session = service.execute(
            user=self.user, ip_address="192.168.1.1", user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0"
        )

        assert session.user == self.user
        assert session.ip_address == "192.168.1.1"
        assert session.is_active is True

    def test_list_sessions(self):
        # Create multiple sessions
        for i in range(3):
            Session.objects.create(user=self.user, ip_address=f"192.168.1.{i}", user_agent="Mozilla/5.0")

        service = ListSessionsService()
        sessions = service.execute(self.user)

        assert len(sessions) == 3

    def test_revoke_session(self):
        session = Session.objects.create(user=self.user, ip_address="192.168.1.1", user_agent="Mozilla/5.0")

        service = RevokeSessionService()
        result = service.execute(self.user, session.id)

        assert result is True
        session.refresh_from_db()
        assert session.is_active is False

    def test_revoke_session_not_owned(self):
        other_user = User.objects.create_user(
            email="other@example.com", password="Password@123", first_name="Other", last_name="User"
        )
        session = Session.objects.create(user=other_user, ip_address="192.168.1.1", user_agent="Mozilla/5.0")

        service = RevokeSessionService()
        result = service.execute(self.user, session.id)

        assert result is False

    def test_revoke_all_sessions(self):
        # Create multiple sessions
        for i in range(3):
            Session.objects.create(user=self.user, ip_address=f"192.168.1.{i}", user_agent="Mozilla/5.0")

        service = RevokeAllSessionsService()
        count = service.execute(self.user)

        assert count == 3
        assert Session.objects.filter(user=self.user, is_active=True).count() == 0

    def test_revoke_all_sessions_except_current(self):
        # Create multiple sessions
        sessions = []
        for i in range(3):
            session = Session.objects.create(user=self.user, ip_address=f"192.168.1.{i}", user_agent="Mozilla/5.0")
            sessions.append(session)

        service = RevokeAllSessionsService()
        count = service.execute(self.user, except_session_id=sessions[0].id)

        assert count == 2
        sessions[0].refresh_from_db()
        assert sessions[0].is_active is True
