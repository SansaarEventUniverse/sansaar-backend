from domain.session_model import Session


class RevokeAllSessionsService:
    def execute(self, user, except_session_id=None):
        """Revoke all sessions for user, optionally except current session"""
        sessions = Session.objects.filter(user=user, is_active=True)
        
        if except_session_id:
            sessions = sessions.exclude(id=except_session_id)
        
        count = 0
        for session in sessions:
            session.revoke()
            count += 1
        
        return count
