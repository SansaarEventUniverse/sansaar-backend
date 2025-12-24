from rest_framework import serializers
from domain.models import SystemHealth, HealthCheck


class SystemHealthSerializer(serializers.ModelSerializer):
    is_critical = serializers.SerializerMethodField()

    class Meta:
        model = SystemHealth
        fields = ['id', 'service_name', 'status', 'cpu_usage', 'memory_usage', 'is_critical', 'created_at']

    def get_is_critical(self, obj):
        return obj.is_critical()


class HealthCheckSerializer(serializers.ModelSerializer):
    is_healthy = serializers.SerializerMethodField()

    class Meta:
        model = HealthCheck
        fields = ['id', 'service_name', 'endpoint', 'status', 'response_time', 'is_healthy', 'checked_at']

    def get_is_healthy(self, obj):
        return obj.is_healthy()
