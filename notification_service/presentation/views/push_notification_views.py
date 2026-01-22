from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from application.services.push_notification_service import PushNotificationService, NotificationSchedulingService, DeviceManagementService
from presentation.serializers.push_notification_serializers import PushNotificationSerializer, DeviceSerializer

@api_view(['POST', 'GET'])
def push_notifications(request):
    """Send or get push notifications"""
    service = PushNotificationService()
    
    if request.method == 'POST':
        device_tokens = request.data.pop('device_tokens', [])
        notification = service.create_notification(request.data)
        
        if device_tokens:
            scheduling_service = NotificationSchedulingService()
            scheduling_service.send_notification(notification.id, device_tokens)
        
        serializer = PushNotificationSerializer(notification)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    notifications = service.get_notifications()
    serializer = PushNotificationSerializer(notifications, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def register_device(request):
    """Register device for push notifications"""
    service = DeviceManagementService()
    device = service.register_device(request.data)
    serializer = DeviceSerializer(device)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
