from rest_framework import serializers

from domain.location import EventLocation


class EventLocationSerializer(serializers.ModelSerializer):
    """Serializer for EventLocation."""
    
    distance_km = serializers.FloatField(read_only=True, required=False)
    
    class Meta:
        model = EventLocation
        fields = [
            'event_id', 'address', 'city', 'state', 'country', 'postal_code',
            'latitude', 'longitude', 'is_verified', 'distance_km'
        ]


class NearbySearchSerializer(serializers.Serializer):
    """Serializer for nearby search parameters."""
    
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    radius_km = serializers.FloatField(default=10.0, min_value=0.1, max_value=500.0)


class LocationSearchSerializer(serializers.Serializer):
    """Serializer for location search parameters."""
    
    city = serializers.CharField(max_length=100, required=False)
    country = serializers.CharField(max_length=100, required=False)
    radius_km = serializers.FloatField(default=50.0, required=False)
