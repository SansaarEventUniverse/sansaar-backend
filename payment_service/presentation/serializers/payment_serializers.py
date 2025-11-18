from rest_framework import serializers
from domain.payment import Payment, PaymentMethod


class PaymentMethodSerializer(serializers.ModelSerializer):
    """Serializer for PaymentMethod."""
    
    class Meta:
        model = PaymentMethod
        fields = ['id', 'name', 'gateway', 'currency', 'is_active']


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for Payment."""
    
    class Meta:
        model = Payment
        fields = [
            'id', 'order_id', 'payment_method', 'amount', 'currency',
            'status', 'gateway_transaction_id', 'refund_amount',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'gateway_transaction_id', 'refund_amount', 'created_at', 'updated_at']


class ProcessPaymentSerializer(serializers.Serializer):
    """Serializer for processing payments."""
    
    order_id = serializers.UUIDField()
    payment_method_id = serializers.UUIDField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField(max_length=3, required=False)


class RefundPaymentSerializer(serializers.Serializer):
    """Serializer for refunding payments."""
    
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    reason = serializers.CharField(required=False, allow_blank=True)
