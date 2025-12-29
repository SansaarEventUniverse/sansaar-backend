from rest_framework import serializers
from domain.models import SecurityEvent, SecurityRule


class SecurityEventSerializer(serializers.ModelSerializer):
    is_critical = serializers.SerializerMethodField()

    class Meta:
        model = SecurityEvent
        fields = ['id', 'event_type', 'severity', 'source_ip', 'description', 'is_critical', 'created_at']

    def get_is_critical(self, obj):
        return obj.is_critical()


class SecurityRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityRule
        fields = ['id', 'name', 'rule_type', 'threshold', 'is_active', 'created_at']
