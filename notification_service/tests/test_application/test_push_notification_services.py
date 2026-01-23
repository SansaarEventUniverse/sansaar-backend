import pytest
from domain.models import PushNotification, NotificationTemplate, Device
from application.services.push_notification_service import PushNotificationService, NotificationSchedulingService, DeviceManagementService

@pytest.mark.django_db
class TestPushNotificationService:
    def test_create_notification(self):
        """Test creating notification"""
        service = PushNotificationService()
        notification = service.create_notification({
            'title': 'Test',
            'body': 'Test Body'
        })
        assert notification.title == 'Test'

    def test_get_notifications(self):
        """Test getting notifications"""
        PushNotification.objects.create(title="Notification 1", body="Body 1")
        PushNotification.objects.create(title="Notification 2", body="Body 2")
        
        service = PushNotificationService()
        notifications = service.get_notifications()
        assert notifications.count() == 2

@pytest.mark.django_db
class TestNotificationSchedulingService:
    def test_send_notification(self):
        """Test sending notification"""
        device = Device.objects.create(user_id=1, device_token="test_token", platform='android')
        notification = PushNotification.objects.create(title="Test", body="Test Body", status='pending')
        
        service = NotificationSchedulingService()
        result = service.send_notification(notification.id, [device.device_token])
        
        assert result is True
        notification.refresh_from_db()
        assert notification.status == 'sent'

@pytest.mark.django_db
class TestDeviceManagementService:
    def test_register_device(self):
        """Test registering device"""
        service = DeviceManagementService()
        device = service.register_device({
            'user_id': 1,
            'device_token': 'test_token_123',
            'platform': 'android'
        })
        assert device.user_id == 1
        assert device.platform == 'android'

    def test_get_user_devices(self):
        """Test getting user devices"""
        Device.objects.create(user_id=1, device_token="token1", platform='android')
        Device.objects.create(user_id=1, device_token="token2", platform='ios')
        Device.objects.create(user_id=2, device_token="token3", platform='android')
        
        service = DeviceManagementService()
        devices = service.get_user_devices(1)
        assert devices.count() == 2
