from domain.session_model import Session


class RevokeSessionService:
    def execute(self, user, session_id):
        """Revoke a specific session"""
        try:
            session = Session.objects.get(id=session_id, user=user, is_active=True)
            session.revoke()
            return True
        except Session.DoesNotExist:
            return False
