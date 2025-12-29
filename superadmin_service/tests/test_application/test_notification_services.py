import pytest
from domain.models import Notification, NotificationRule
from application.services.notification_service import NotificationService


@pytest.mark.django_db
class TestNotificationService:
    def test_create_notification(self):
        service = NotificationService()
        notification = service.create_notification("Alert", "Test message", "alert")
        assert notification.title == "Alert"

    def test_get_unread_notifications(self):
        Notification.objects.create(title="Test", message="Msg", notification_type="info", status="unread")
        service = NotificationService()
        unread = service.get_unread_notifications()
        assert len(unread) == 1
