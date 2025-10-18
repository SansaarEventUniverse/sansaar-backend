from rest_framework import serializers
from domain.event import Event, EventDraft


class EventSerializer(serializers.ModelSerializer):
    """Serializer for Event model."""
    
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'status', 'visibility',
            'organizer_id', 'organization_id',
            'start_datetime', 'end_datetime', 'timezone', 'is_all_day',
            'venue_id', 'is_online', 'online_url', 'max_attendees',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate(self, data):
        """Validate event data."""
        if data.get('end_datetime') and data.get('start_datetime'):
            if data['start_datetime'] >= data['end_datetime']:
                raise serializers.ValidationError({
                    'end_datetime': 'End datetime must be after start datetime'
                })
        
        if data.get('is_online') and not data.get('online_url'):
            raise serializers.ValidationError({
                'online_url': 'Online URL is required for online events'
            })
        
        if not data.get('is_online') and not data.get('venue_id'):
            raise serializers.ValidationError({
                'venue_id': 'Venue is required for in-person events'
            })
        
        return data


class EventDraftSerializer(serializers.ModelSerializer):
    """Serializer for EventDraft model."""
    
    class Meta:
        model = EventDraft
        fields = ['id', 'event_id', 'organizer_id', 'draft_data', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
