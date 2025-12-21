from rest_framework import serializers
from domain.models import PerformanceMetric, SystemHealth


class PerformanceMetricSerializer(serializers.ModelSerializer):
    is_healthy = serializers.SerializerMethodField()

    class Meta:
        model = PerformanceMetric
        fields = ['id', 'metric_name', 'metric_value', 'metric_unit', 'threshold', 'is_healthy', 'created_at']

    def get_is_healthy(self, obj):
        return obj.is_healthy()


class SystemHealthSerializer(serializers.ModelSerializer):
    is_critical = serializers.SerializerMethodField()

    class Meta:
        model = SystemHealth
        fields = ['id', 'service_name', 'status', 'cpu_usage', 'memory_usage', 'is_critical', 'created_at']

    def get_is_critical(self, obj):
        return obj.is_critical()
