from rest_framework import serializers

from domain.search_index import EventSearchIndex


class EventSearchResultSerializer(serializers.ModelSerializer):
    """Serializer for event search results."""
    
    class Meta:
        model = EventSearchIndex
        fields = [
            'event_id', 'title', 'description', 'category', 'tags',
            'location', 'city', 'status', 'search_rank', 'view_count',
            'event_date', 'created_at'
        ]


class SearchFiltersSerializer(serializers.Serializer):
    """Serializer for search filters."""
    
    categories = serializers.ListField(child=serializers.CharField())
    cities = serializers.ListField(child=serializers.CharField())
    statuses = serializers.ListField(child=serializers.CharField())
