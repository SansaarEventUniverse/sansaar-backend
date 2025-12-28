import pytest
from domain.models import Notification
from infrastructure.notifications.notification_dispatcher import NotificationDispatcher


@pytest.mark.django_db
class TestNotificationDispatcher:
    def test_dispatch_notification(self):
        notification = Notification.objects.create(
            title="Test",
            message="Test message",
            notification_type="info"
        )
        dispatcher = NotificationDispatcher()
        result = dispatcher.dispatch(notification.id)
        assert result["status"] == "dispatched"
