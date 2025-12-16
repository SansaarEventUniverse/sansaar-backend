from domain.models import UserActivity


class UserActivityTracker:
    def track(self, user_id: str, activity_type: str, event_id: str = None):
        return UserActivity.objects.create(
            user_id=user_id,
            activity_type=activity_type,
            event_id=event_id
        )
