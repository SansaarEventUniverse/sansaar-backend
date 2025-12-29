from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from domain.models import Notification, NotificationRule
from presentation.serializers.notification_serializers import NotificationSerializer, NotificationRuleSerializer


class GetNotificationsView(APIView):
    def get(self, request):
        notifications = Notification.objects.all().order_by('-created_at')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)


class CreateNotificationView(APIView):
    def post(self, request):
        serializer = NotificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class NotificationRulesView(APIView):
    def get(self, request):
        rules = NotificationRule.objects.all()
        serializer = NotificationRuleSerializer(rules, many=True)
        return Response(serializer.data)
