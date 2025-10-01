from domain.session_model import Session


class ListSessionsService:
    def execute(self, user):
        """List all active sessions for user"""
        return Session.objects.filter(user=user, is_active=True).order_by('-last_activity_at')
