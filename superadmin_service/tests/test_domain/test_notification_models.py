import pytest
from domain.notification_model import Notification, NotificationRule


@pytest.mark.django_db
class TestNotificationModel:
    def test_create_notification(self):
        notification = Notification.objects.create(
            title="System Alert",
            message="High CPU usage detected",
            notification_type="alert",
            status="unread"
        )
        assert notification.title == "System Alert"
        assert notification.is_unread() is True

    def test_mark_as_read(self):
        notification = Notification.objects.create(
            title="Test",
            message="Test message",
            notification_type="info",
            status="unread"
        )
        notification.status = "read"
        notification.save()
        assert notification.is_unread() is False


@pytest.mark.django_db
class TestNotificationRuleModel:
    def test_create_notification_rule(self):
        rule = NotificationRule.objects.create(
            name="CPU Alert Rule",
            condition="cpu_usage > 90",
            notification_type="alert",
            is_active=True
        )
        assert rule.name == "CPU Alert Rule"
        assert rule.is_active is True
