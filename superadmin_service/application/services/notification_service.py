from domain.models import Notification


class NotificationService:
    def create_notification(self, title: str, message: str, notification_type: str):
        return Notification.objects.create(
            title=title,
            message=message,
            notification_type=notification_type,
            status="unread"
        )

    def get_unread_notifications(self):
        return list(Notification.objects.filter(status="unread"))
