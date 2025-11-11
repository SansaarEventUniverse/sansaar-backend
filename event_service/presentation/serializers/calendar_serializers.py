from rest_framework import serializers

from domain.calendar import CalendarEvent


class CalendarEventSerializer(serializers.ModelSerializer):
    """Serializer for CalendarEvent."""
    
    class Meta:
        model = CalendarEvent
        fields = [
            'id', 'event_id', 'provider', 'sync_status', 
            'external_event_id', 'last_synced_at', 'created_at'
        ]


class SyncCalendarSerializer(serializers.Serializer):
    """Serializer for calendar sync request."""
    
    provider = serializers.ChoiceField(choices=CalendarEvent.CALENDAR_PROVIDER)
    external_calendar_id = serializers.CharField(max_length=255, required=False, allow_blank=True)
    user_id = serializers.UUIDField()


class CalendarWebhookSerializer(serializers.Serializer):
    """Serializer for calendar webhook payload."""
    
    event_id = serializers.CharField(max_length=255)
    action = serializers.CharField(max_length=50)
    provider = serializers.CharField(max_length=20)
