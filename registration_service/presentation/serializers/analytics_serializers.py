from rest_framework import serializers

from domain.analytics import RegistrationAnalytics


class RegistrationAnalyticsSerializer(serializers.ModelSerializer):
    """Serializer for RegistrationAnalytics."""
    
    conversion_rate = serializers.SerializerMethodField()
    
    class Meta:
        model = RegistrationAnalytics
        fields = [
            'event_id', 'total_registrations', 'confirmed_registrations',
            'cancelled_registrations', 'total_waitlist', 'promoted_from_waitlist',
            'total_groups', 'total_group_members', 'capacity_utilization',
            'conversion_rate', 'last_updated'
        ]
    
    def get_conversion_rate(self, obj):
        return float(obj.get_conversion_rate())
