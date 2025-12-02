from celery import shared_task

from infrastructure.messaging.user_registered_event_handler import UserRegisteredEventHandler


@shared_task(name="user.registered")
def create_user_profile(user_data):
    """Create user profile when user registers"""
    handler = UserRegisteredEventHandler()
    handler.handle(user_data)
    return f"Profile created for user {user_data.get('user_id')}"
