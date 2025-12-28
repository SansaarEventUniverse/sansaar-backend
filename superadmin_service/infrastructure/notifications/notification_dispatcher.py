from domain.models import Notification


class NotificationDispatcher:
    def dispatch(self, notification_id: int):
        notification = Notification.objects.get(id=notification_id)
        return {
            "notification_id": notification_id,
            "status": "dispatched",
            "title": notification.title
        }
