from domain.models import UserAnalytics


class UserRepository:
    def get_all_users(self):
        return list(UserAnalytics.objects.all())
