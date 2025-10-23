from rest_framework import serializers
from domain.venue import Venue


class VenueSerializer(serializers.ModelSerializer):
    """Serializer for Venue model."""
    
    class Meta:
        model = Venue
        fields = [
            'id', 'name', 'description', 'address', 'city', 'state', 
            'country', 'postal_code', 'latitude', 'longitude', 'capacity',
            'is_verified', 'verified_at', 'owner_id', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'is_verified', 'verified_at', 'created_at', 'updated_at']
    
    def validate_capacity(self, value):
        """Validate capacity is positive."""
        if value < 1:
            raise serializers.ValidationError('Capacity must be at least 1')
        return value
