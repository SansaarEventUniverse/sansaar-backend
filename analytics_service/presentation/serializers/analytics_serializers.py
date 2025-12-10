from rest_framework import serializers
from domain.models import AnalyticsEvent, MetricCalculation


class AnalyticsEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyticsEvent
        fields = ['id', 'event_type', 'event_data', 'user_id', 'session_id', 'is_processed', 'created_at']
        read_only_fields = ['id', 'is_processed', 'created_at']


class MetricCalculationSerializer(serializers.ModelSerializer):
    percentage_change = serializers.SerializerMethodField()

    class Meta:
        model = MetricCalculation
        fields = ['id', 'metric_name', 'metric_value', 'previous_value', 'calculation_type', 
                  'time_period', 'percentage_change', 'created_at']

    def get_percentage_change(self, obj):
        return obj.calculate_percentage_change()


class AnalyticsQuerySerializer(serializers.Serializer):
    event_type = serializers.CharField(required=False)
    user_id = serializers.CharField(required=False)
    time_period = serializers.CharField(required=False)
    start_date = serializers.DateTimeField(required=False)
    end_date = serializers.DateTimeField(required=False)
