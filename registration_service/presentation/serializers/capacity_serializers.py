from rest_framework import serializers
from domain.capacity_rule import CapacityRule


class CapacityRuleSerializer(serializers.ModelSerializer):
    """Serializer for CapacityRule model."""
    
    class Meta:
        model = CapacityRule
        fields = [
            'id', 'event_id', 'max_capacity', 'warning_threshold',
            'allow_reservations', 'reservation_timeout_minutes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
