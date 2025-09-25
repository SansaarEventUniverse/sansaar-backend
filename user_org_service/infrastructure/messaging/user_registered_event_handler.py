from domain.user_profile_model import UserProfile


class UserRegisteredEventHandler:
    def handle(self, event_data):
        user_id = event_data["user_id"]

        # Check if profile already exists
        if UserProfile.objects.filter(user_id=user_id).exists():
            return

        UserProfile.objects.create(
            user_id=user_id,
            email=event_data["email"],
            first_name=event_data["first_name"],
            last_name=event_data["last_name"],
        )
