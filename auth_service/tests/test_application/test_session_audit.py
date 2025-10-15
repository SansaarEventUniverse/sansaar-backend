import pytest

from application.create_session_service import CreateSessionService
from application.revoke_all_sessions_service import RevokeAllSessionsService
from application.revoke_session_service import RevokeSessionService
from domain.audit_log_model import AuditEventType, AuditLog
from domain.session_model import Session
from domain.user_model import User


@pytest.mark.django_db
class TestSessionAudit:
    def setup_method(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="Password@123", first_name="Test", last_name="User"
        )

    def test_session_created_event_logged(self):
        service = CreateSessionService()
        session = service.execute(user=self.user, ip_address="192.168.1.1", user_agent="Mozilla/5.0")

        # Check audit log
        audit = AuditLog.objects.filter(event_type=AuditEventType.SESSION_CREATED, user_id=str(self.user.id)).first()

        assert audit is not None
        assert audit.metadata["session_id"] == str(session.id)

    def test_session_revoked_event_logged(self):
        session = Session.objects.create(user=self.user, ip_address="192.168.1.1", user_agent="Mozilla/5.0")

        service = RevokeSessionService()
        service.execute(self.user, session.id)

        # Check audit log
        audit = AuditLog.objects.filter(event_type=AuditEventType.SESSION_REVOKED, user_id=str(self.user.id)).first()

        assert audit is not None
        assert audit.metadata["session_id"] == str(session.id)

    def test_bulk_session_revoked_event_logged(self):
        # Create multiple sessions
        for i in range(3):
            Session.objects.create(user=self.user, ip_address=f"192.168.1.{i}", user_agent="Mozilla/5.0")

        service = RevokeAllSessionsService()
        service.execute(self.user)

        # Check audit log
        audit = AuditLog.objects.filter(event_type=AuditEventType.SESSION_REVOKED, user_id=str(self.user.id)).first()

        assert audit is not None
        assert audit.metadata["revoked_count"] == 3
