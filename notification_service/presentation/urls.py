from django.urls import path
from presentation.views.health_views import health_check
from presentation.views.push_notification_views import push_notifications, register_device

urlpatterns = [
    # Health Check
    path('health/', health_check, name='health_check'),
    
    # Push Notifications
    path('push-notifications/', push_notifications, name='push_notifications'),
    path('devices/register/', register_device, name='register_device'),
]
