import pytest
from rest_framework.test import APIClient
from domain.models import PushNotification, Device

@pytest.mark.django_db
class TestPushNotificationAPI:
    def setup_method(self):
        self.client = APIClient()

    def test_send_notification(self):
        """Test sending notification via API"""
        Device.objects.create(user_id=1, device_token="test_token", platform='android')
        
        data = {
            'title': 'Test Notification',
            'body': 'Test Body',
            'device_tokens': ['test_token']
        }
        response = self.client.post('/api/notifications/push-notifications/', data, format='json')
        assert response.status_code == 201
        assert response.data['title'] == 'Test Notification'

    def test_get_notifications(self):
        """Test getting notifications"""
        PushNotification.objects.create(title="Notification 1", body="Body 1")
        PushNotification.objects.create(title="Notification 2", body="Body 2")
        
        response = self.client.get('/api/notifications/push-notifications/')
        assert response.status_code == 200
        assert len(response.data) == 2

    def test_register_device(self):
        """Test registering device"""
        data = {
            'user_id': 1,
            'device_token': 'test_token_123',
            'platform': 'android'
        }
        response = self.client.post('/api/notifications/devices/register/', data, format='json')
        assert response.status_code == 201
        assert response.data['device_token'] == 'test_token_123'
