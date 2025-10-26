from rest_framework import serializers
from domain.waitlist import Waitlist


class WaitlistSerializer(serializers.ModelSerializer):
    """Serializer for Waitlist model."""
    
    class Meta:
        model = Waitlist
        fields = [
            'id', 'event_id', 'user_id', 'position', 'priority',
            'is_promoted', 'promoted_at', 'joined_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'position', 'is_promoted', 'promoted_at', 'joined_at', 'created_at', 'updated_at']
