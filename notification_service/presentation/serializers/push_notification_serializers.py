from rest_framework import serializers
from domain.models import PushNotification, NotificationTemplate, Device

class NotificationTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationTemplate
        fields = ['id', 'name', 'title', 'body', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'user_id', 'device_token', 'platform', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class PushNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushNotification
        fields = ['id', 'title', 'body', 'template', 'data', 'status', 'sent_at', 'created_at', 'updated_at']
        read_only_fields = ['id', 'status', 'sent_at', 'created_at', 'updated_at']
