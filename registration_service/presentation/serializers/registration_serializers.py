from rest_framework import serializers
from domain.registration import Registration


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer for Registration model."""
    
    class Meta:
        model = Registration
        fields = [
            'id', 'event_id', 'user_id', 'status',
            'attendee_name', 'attendee_email', 'attendee_phone',
            'registered_at', 'cancelled_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'registered_at', 'cancelled_at', 'created_at', 'updated_at']
