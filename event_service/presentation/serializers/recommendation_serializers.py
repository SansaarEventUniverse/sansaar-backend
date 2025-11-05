from rest_framework import serializers

from domain.recommendation import UserPreference


class UserPreferenceSerializer(serializers.ModelSerializer):
    """Serializer for UserPreference."""
    
    class Meta:
        model = UserPreference
        fields = [
            'user_id', 'preferred_categories', 'preferred_tags',
            'preferred_cities', 'max_distance_km'
        ]


class UpdatePreferencesSerializer(serializers.Serializer):
    """Serializer for updating preferences."""
    
    preferred_categories = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )
    preferred_tags = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )
    preferred_cities = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )
    max_distance_km = serializers.FloatField(required=False)


class RecommendationSerializer(serializers.Serializer):
    """Serializer for recommendation results."""
    
    event_id = serializers.UUIDField()
    title = serializers.CharField()
    category = serializers.CharField()
    score = serializers.FloatField()
    reason = serializers.CharField()
