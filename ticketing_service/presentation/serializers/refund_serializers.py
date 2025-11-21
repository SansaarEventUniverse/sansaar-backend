from rest_framework import serializers
from domain.refund import Refund, RefundPolicy


class RequestRefundSerializer(serializers.Serializer):
    """Serializer for requesting refunds."""
    ticket_id = serializers.UUIDField()
    original_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    reason = serializers.CharField()


class ProcessRefundSerializer(serializers.Serializer):
    """Serializer for processing refunds."""
    action = serializers.ChoiceField(choices=['approve', 'reject'])
    rejection_reason = serializers.CharField(required=False, allow_blank=True)


class RefundSerializer(serializers.ModelSerializer):
    """Serializer for refund responses."""
    
    class Meta:
        model = Refund
        fields = ['id', 'ticket_id', 'order_id', 'payment_id', 'original_amount',
                  'refund_amount', 'processing_fee', 'reason', 'status',
                  'rejected_reason', 'processed_at', 'created_at', 'updated_at']


class RefundPolicySerializer(serializers.ModelSerializer):
    """Serializer for refund policy responses."""
    
    class Meta:
        model = RefundPolicy
        fields = ['id', 'event_id', 'refund_allowed', 'refund_before_hours',
                  'refund_percentage', 'processing_fee', 'created_at']
