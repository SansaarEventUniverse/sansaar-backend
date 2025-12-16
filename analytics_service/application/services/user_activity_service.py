from django.db import transaction
from domain.models import UserActivity


class UserActivityService:
    @transaction.atomic
    def track_activity(self, user_id: str, activity_type: str, event_id: str = None):
        return UserActivity.objects.create(
            user_id=user_id,
            activity_type=activity_type,
            event_id=event_id
        )

    def get_user_activities(self, user_id: str):
        return list(UserActivity.get_user_activities(user_id))
