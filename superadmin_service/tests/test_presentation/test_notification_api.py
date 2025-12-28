import pytest
from rest_framework.test import APIClient
from domain.models import Notification, NotificationRule


@pytest.mark.django_db
class TestNotificationAPI:
    def test_get_notifications(self):
        Notification.objects.create(title="Test", message="Message", notification_type="info", status="unread")
        client = APIClient()
        response = client.get('/api/superadmin/admin/notifications/')
        assert response.status_code == 200
        assert len(response.data) == 1

    def test_create_notification(self):
        client = APIClient()
        response = client.post('/api/superadmin/admin/notifications/create/', {
            'title': 'New Alert',
            'message': 'Test message',
            'notification_type': 'alert'
        }, format='json')
        assert response.status_code == 201

    def test_notification_rules(self):
        NotificationRule.objects.create(name="Test Rule", condition="cpu > 90", notification_type="alert", is_active=True)
        client = APIClient()
        response = client.get('/api/superadmin/admin/notification-rules/')
        assert response.status_code == 200
        assert len(response.data) == 1
