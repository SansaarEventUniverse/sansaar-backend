from rest_framework import serializers


class ValidateOfflineSerializer(serializers.Serializer):
    """Serializer for offline validation."""
    qr_code = serializers.CharField(max_length=255)


class SyncTicketDataSerializer(serializers.Serializer):
    """Serializer for ticket sync."""
    event_id = serializers.UUIDField()
    tickets = serializers.ListField(child=serializers.DictField())


class OfflineStatusSerializer(serializers.Serializer):
    """Serializer for offline status."""
    event_id = serializers.UUIDField()
    ticket_count = serializers.IntegerField()
    last_synced = serializers.DateTimeField()
    cache_status = serializers.CharField()
