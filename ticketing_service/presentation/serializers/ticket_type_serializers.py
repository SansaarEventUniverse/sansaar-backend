from rest_framework import serializers
from domain.ticket_type import TicketType


class TicketTypeSerializer(serializers.ModelSerializer):
    """Serializer for TicketType model."""
    
    available_quantity = serializers.IntegerField(read_only=True)
    is_available = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = TicketType
        fields = [
            'id', 'event_id', 'name', 'description', 'price', 'currency',
            'quantity', 'quantity_sold', 'available_quantity', 'min_purchase',
            'max_purchase', 'sale_start', 'sale_end', 'is_active', 'is_available',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'quantity_sold', 'created_at', 'updated_at']
    
    def to_representation(self, instance):
        """Add computed fields to representation."""
        data = super().to_representation(instance)
        data['available_quantity'] = instance.available_quantity()
        data['is_available'] = instance.is_available()
        return data


class CreateTicketTypeSerializer(serializers.Serializer):
    """Serializer for creating ticket types."""
    
    event_id = serializers.UUIDField()
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(required=False, allow_blank=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField(max_length=3, default='USD')
    quantity = serializers.IntegerField(min_value=0)
    min_purchase = serializers.IntegerField(min_value=1, default=1)
    max_purchase = serializers.IntegerField(min_value=1, default=10)
    sale_start = serializers.DateTimeField()
    sale_end = serializers.DateTimeField()


class UpdateTicketTypeSerializer(serializers.Serializer):
    """Serializer for updating ticket types."""
    
    name = serializers.CharField(max_length=100, required=False)
    description = serializers.CharField(required=False, allow_blank=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    quantity = serializers.IntegerField(min_value=0, required=False)
    min_purchase = serializers.IntegerField(min_value=1, required=False)
    max_purchase = serializers.IntegerField(min_value=1, required=False)
    sale_start = serializers.DateTimeField(required=False)
    sale_end = serializers.DateTimeField(required=False)
    is_active = serializers.BooleanField(required=False)
