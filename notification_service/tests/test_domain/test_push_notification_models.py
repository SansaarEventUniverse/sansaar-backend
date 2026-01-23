import pytest
from domain.models import PushNotification, NotificationTemplate, Device

@pytest.mark.django_db
class TestPushNotification:
    def test_create_notification(self):
        """Test creating push notification"""
        notification = PushNotification.objects.create(
            title="Test Notification",
            body="Test Body",
            status='pending'
        )
        assert notification.title == "Test Notification"
        assert notification.status == 'pending'

    def test_notification_status_choices(self):
        """Test notification status validation"""
        notification = PushNotification.objects.create(title="Test", body="Test", status='sent')
        assert notification.status in ['pending', 'sent', 'failed']

    def test_mark_sent(self):
        """Test marking notification as sent"""
        notification = PushNotification.objects.create(title="Test", body="Test", status='pending')
        notification.mark_sent()
        assert notification.status == 'sent'

    def test_mark_failed(self):
        """Test marking notification as failed"""
        notification = PushNotification.objects.create(title="Test", body="Test", status='pending')
        notification.mark_failed()
        assert notification.status == 'failed'

@pytest.mark.django_db
class TestNotificationTemplate:
    def test_create_template(self):
        """Test creating notification template"""
        template = NotificationTemplate.objects.create(
            name="Welcome Template",
            title="Welcome {{name}}",
            body="Hello {{name}}, welcome!"
        )
        assert template.name == "Welcome Template"
        assert "{{name}}" in template.title

    def test_render_template(self):
        """Test template rendering"""
        template = NotificationTemplate.objects.create(
            name="Test",
            title="Hello {{name}}",
            body="Welcome {{name}}"
        )
        rendered = template.render({'name': 'John'})
        assert rendered['title'] == "Hello John"
        assert rendered['body'] == "Welcome John"

@pytest.mark.django_db
class TestDevice:
    def test_create_device(self):
        """Test creating device"""
        device = Device.objects.create(
            user_id=1,
            device_token="test_token_123",
            platform='android'
        )
        assert device.user_id == 1
        assert device.platform == 'android'

    def test_device_platform_choices(self):
        """Test device platform validation"""
        device = Device.objects.create(user_id=1, device_token="token", platform='ios')
        assert device.platform in ['android', 'ios', 'web']
