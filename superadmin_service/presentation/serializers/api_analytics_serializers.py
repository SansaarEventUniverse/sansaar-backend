from rest_framework import serializers
from domain.models import APIUsage, APIMetrics


class APIUsageSerializer(serializers.ModelSerializer):
    is_successful = serializers.SerializerMethodField()

    class Meta:
        model = APIUsage
        fields = ['id', 'endpoint', 'method', 'status_code', 'response_time', 'is_successful', 'timestamp']

    def get_is_successful(self, obj):
        return obj.is_successful()


class APIMetricsSerializer(serializers.ModelSerializer):
    success_rate = serializers.SerializerMethodField()

    class Meta:
        model = APIMetrics
        fields = ['id', 'endpoint', 'total_requests', 'successful_requests', 'failed_requests', 'avg_response_time', 'success_rate', 'created_at']

    def get_success_rate(self, obj):
        return obj.success_rate()
