from rest_framework import serializers


class AuditLogSerializer(serializers.Serializer):
    event_type = serializers.CharField()
    admin_id = serializers.CharField()
    email = serializers.CharField()
    ip_address = serializers.CharField()
    timestamp = serializers.CharField()
    metadata = serializers.DictField()
