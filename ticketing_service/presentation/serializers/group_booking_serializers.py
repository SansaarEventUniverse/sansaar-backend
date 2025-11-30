from rest_framework import serializers


class CreateGroupBookingSerializer(serializers.Serializer):
    """Serializer for creating group booking."""
    event_id = serializers.UUIDField()
    organizer_id = serializers.UUIDField()
    group_name = serializers.CharField(max_length=255)
    min_participants = serializers.IntegerField(min_value=2)
    max_participants = serializers.IntegerField(min_value=2)


class JoinGroupBookingSerializer(serializers.Serializer):
    """Serializer for joining group booking."""
    user_id = serializers.UUIDField()


class ProcessGroupPaymentSerializer(serializers.Serializer):
    """Serializer for processing group payment."""
    base_price = serializers.DecimalField(max_digits=10, decimal_places=2)


class GroupBookingResponseSerializer(serializers.Serializer):
    """Serializer for group booking response."""
    booking_id = serializers.UUIDField()
    group_name = serializers.CharField()
    current_participants = serializers.IntegerField()
    status = serializers.CharField()
