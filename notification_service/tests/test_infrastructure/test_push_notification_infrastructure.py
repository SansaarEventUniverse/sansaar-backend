import pytest
from domain.models import PushNotification, Device
from infrastructure.repositories.push_notification_repository import PushNotificationRepository

@pytest.mark.django_db
class TestPushNotificationRepository:
    def test_get_notification_analytics(self):
        """Test getting notification analytics"""
        PushNotification.objects.create(title="Notification 1", body="Body 1", status='sent')
        PushNotification.objects.create(title="Notification 2", body="Body 2", status='pending')
        
        repo = PushNotificationRepository()
        analytics = repo.get_notification_analytics()
        
        assert analytics['total_notifications'] == 2
        assert analytics['sent_notifications'] == 1

    def test_get_notifications_by_status(self):
        """Test getting notifications by status"""
        PushNotification.objects.create(title="Notification 1", body="Body 1", status='sent')
        PushNotification.objects.create(title="Notification 2", body="Body 2", status='sent')
        PushNotification.objects.create(title="Notification 3", body="Body 3", status='pending')
        
        repo = PushNotificationRepository()
        sent_notifications = repo.get_notifications_by_status('sent')
        
        assert sent_notifications.count() == 2
