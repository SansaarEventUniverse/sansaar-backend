from application.log_audit_event_service import LogAuditEventService
from domain.audit_log_model import AuditEventType
from domain.session_model import Session


class RevokeSessionService:
    def __init__(self):
        self.audit_service = LogAuditEventService()

    def execute(self, user, session_id):
        """Revoke a specific session"""
        try:
            session = Session.objects.get(id=session_id, user=user, is_active=True)
            session.revoke()

            # Log session revocation
            self.audit_service.log_event(
                event_type=AuditEventType.SESSION_REVOKED,
                user_id=str(user.id),
                metadata={"session_id": str(session.id)},
            )

            return True
        except Session.DoesNotExist:
            return False
