from rest_framework import serializers
from domain.order import Order, OrderItem


class OrderItemSerializer(serializers.Serializer):
    """Serializer for order items."""
    ticket_type_id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1)


class CreateOrderSerializer(serializers.Serializer):
    """Serializer for creating orders."""
    user_id = serializers.UUIDField()
    event_id = serializers.UUIDField()
    items = OrderItemSerializer(many=True)
    currency = serializers.CharField(max_length=3, default='USD')


class ProcessPurchaseSerializer(serializers.Serializer):
    """Serializer for processing purchases."""
    payment_id = serializers.UUIDField()


class OrderItemResponseSerializer(serializers.ModelSerializer):
    """Serializer for order item responses."""
    
    class Meta:
        model = OrderItem
        fields = ['id', 'ticket_type_id', 'quantity', 'unit_price', 'subtotal']


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for order responses."""
    items = OrderItemResponseSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'user_id', 'event_id', 'total_amount', 'currency', 
                  'status', 'payment_id', 'items', 'created_at', 'updated_at']
