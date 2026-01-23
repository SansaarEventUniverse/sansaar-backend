from domain.models import PushNotification, NotificationTemplate, Device
from infrastructure.fcm.fcm_service import FCMService

class PushNotificationService:
    def create_notification(self, data):
        return PushNotification.objects.create(**data)

    def get_notifications(self):
        return PushNotification.objects.all()

    def get_notification(self, notification_id):
        return PushNotification.objects.get(id=notification_id)

class NotificationSchedulingService:
    def __init__(self):
        try:
            self.fcm_service = FCMService()
        except Exception:
            self.fcm_service = None

    def send_notification(self, notification_id, device_tokens):
        notification = PushNotification.objects.get(id=notification_id)
        try:
            if self.fcm_service:
                for token in device_tokens:
                    self.fcm_service.send_push_notification(token, notification.title, notification.body, notification.data)
            notification.mark_sent()
            return True
        except Exception:
            notification.mark_failed()
            return False

class DeviceManagementService:
    def register_device(self, data):
        device, created = Device.objects.update_or_create(
            device_token=data['device_token'],
            defaults=data
        )
        return device

    def get_user_devices(self, user_id):
        return Device.objects.filter(user_id=user_id, is_active=True)

    def deactivate_device(self, device_token):
        device = Device.objects.get(device_token=device_token)
        device.is_active = False
        device.save()
        return device
