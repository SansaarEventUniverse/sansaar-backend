from application.log_audit_event_service import LogAuditEventService
from domain.audit_log_model import AuditEventType
from domain.session_model import Session


class RevokeAllSessionsService:
    def __init__(self):
        self.audit_service = LogAuditEventService()

    def execute(self, user, except_session_id=None):
        """Revoke all sessions for user, optionally except current session"""
        sessions = Session.objects.filter(user=user, is_active=True)
        
        if except_session_id:
            sessions = sessions.exclude(id=except_session_id)
        
        count = 0
        session_ids = []
        for session in sessions:
            session.revoke()
            session_ids.append(str(session.id))
            count += 1
        
        # Log bulk session revocation
        if count > 0:
            self.audit_service.log_event(
                event_type=AuditEventType.SESSION_REVOKED,
                user_id=str(user.id),
                metadata={
                    'revoked_count': count,
                    'session_ids': session_ids,
                    'except_session_id': str(except_session_id) if except_session_id else None
                }
            )
        
        return count
