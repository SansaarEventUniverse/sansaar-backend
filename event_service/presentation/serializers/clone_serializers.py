from rest_framework import serializers

from domain.event import Event
from domain.clone import EventClone


class CloneEventSerializer(serializers.Serializer):
    """Serializer for cloning event."""
    
    cloned_by = serializers.UUIDField()
    customizations = serializers.JSONField(required=False)
    reason = serializers.CharField(max_length=255, required=False, allow_blank=True)


class BulkCloneSerializer(serializers.Serializer):
    """Serializer for bulk cloning."""
    
    event_ids = serializers.ListField(child=serializers.UUIDField())
    cloned_by = serializers.UUIDField()
    customizations = serializers.JSONField(required=False)


class CloneSeriesSerializer(serializers.Serializer):
    """Serializer for cloning event series."""
    
    cloned_by = serializers.UUIDField()
    count = serializers.IntegerField(min_value=1, max_value=50)
    interval_days = serializers.IntegerField(min_value=1, default=7)


class EventCloneInfoSerializer(serializers.ModelSerializer):
    """Serializer for EventClone."""
    
    class Meta:
        model = EventClone
        fields = ['id', 'original_event_id', 'cloned_event_id', 'cloned_by', 
                 'clone_reason', 'fields_modified', 'created_at']
