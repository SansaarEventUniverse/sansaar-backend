from domain.models import UserAnalytics


class UserManagementService:
    def get_user_analytics(self, user_id: str):
        return UserAnalytics.objects.get(user_id=user_id)
