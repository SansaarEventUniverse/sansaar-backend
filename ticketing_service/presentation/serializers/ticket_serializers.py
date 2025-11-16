from rest_framework import serializers
from domain.ticket import Ticket


class TicketSerializer(serializers.ModelSerializer):
    """Serializer for Ticket model."""
    
    class Meta:
        model = Ticket
        fields = [
            'id', 'ticket_type_id', 'order_id', 'attendee_name', 'attendee_email',
            'qr_code_data', 'status', 'checked_in_at', 'checked_in_by',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'qr_code_data', 'security_hash', 'checked_in_at', 'checked_in_by', 'created_at', 'updated_at']


class ValidateQRCodeSerializer(serializers.Serializer):
    """Serializer for QR code validation."""
    
    qr_code_data = serializers.CharField()


class CheckInSerializer(serializers.Serializer):
    """Serializer for ticket check-in."""
    
    checked_in_by = serializers.UUIDField()
