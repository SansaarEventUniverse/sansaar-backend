from rest_framework import serializers
from domain.models import Notification, NotificationRule


class NotificationSerializer(serializers.ModelSerializer):
    is_unread = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'notification_type', 'status', 'is_unread', 'created_at']

    def get_is_unread(self, obj):
        return obj.is_unread()


class NotificationRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationRule
        fields = ['id', 'name', 'condition', 'notification_type', 'is_active', 'created_at']
