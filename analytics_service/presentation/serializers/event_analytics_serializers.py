from rest_framework import serializers
from domain.models import EventMetrics, AttendanceAnalytics


class EventMetricsSerializer(serializers.ModelSerializer):
    conversion_rate = serializers.SerializerMethodField()
    attendance_rate = serializers.SerializerMethodField()

    class Meta:
        model = EventMetrics
        fields = ['event_id', 'total_views', 'total_registrations', 'total_attendance', 
                  'revenue', 'conversion_rate', 'attendance_rate', 'created_at', 'updated_at']

    def get_conversion_rate(self, obj):
        return obj.calculate_conversion_rate()

    def get_attendance_rate(self, obj):
        return obj.calculate_attendance_rate()


class AttendanceAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceAnalytics
        fields = ['event_id', 'user_id', 'check_in_time', 'check_out_time', 'is_checked_in', 'created_at']


class CheckInSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100)


class CheckOutSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100)
