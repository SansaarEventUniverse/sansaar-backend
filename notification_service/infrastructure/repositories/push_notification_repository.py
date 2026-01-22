from domain.models import PushNotification

class PushNotificationRepository:
    def get_notification_analytics(self):
        total = PushNotification.objects.count()
        sent = PushNotification.objects.filter(status='sent').count()
        
        return {
            'total_notifications': total,
            'sent_notifications': sent,
            'pending_notifications': PushNotification.objects.filter(status='pending').count(),
            'failed_notifications': PushNotification.objects.filter(status='failed').count()
        }

    def get_notifications_by_status(self, status):
        return PushNotification.objects.filter(status=status)
