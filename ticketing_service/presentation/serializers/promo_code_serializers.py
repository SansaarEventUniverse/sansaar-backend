from rest_framework import serializers
from domain.promo_code import PromoCode


class CreatePromoCodeSerializer(serializers.Serializer):
    """Serializer for creating promo codes."""
    code = serializers.CharField(max_length=50)
    event_id = serializers.UUIDField(required=False, allow_null=True)
    discount_type = serializers.ChoiceField(choices=['percentage', 'fixed'])
    discount_value = serializers.DecimalField(max_digits=10, decimal_places=2)
    max_uses = serializers.IntegerField(default=0)
    valid_from = serializers.DateTimeField()
    valid_until = serializers.DateTimeField()
    min_purchase_amount = serializers.DecimalField(max_digits=10, decimal_places=2, default=0)


class ValidatePromoCodeSerializer(serializers.Serializer):
    """Serializer for validating promo codes."""
    code = serializers.CharField(max_length=50)
    order_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    event_id = serializers.UUIDField(required=False, allow_null=True)


class ApplyPromoCodeSerializer(serializers.Serializer):
    """Serializer for applying promo codes."""
    promo_code = serializers.CharField(max_length=50)


class PromoCodeSerializer(serializers.ModelSerializer):
    """Serializer for promo code responses."""
    remaining_uses = serializers.SerializerMethodField()
    
    class Meta:
        model = PromoCode
        fields = ['id', 'code', 'event_id', 'discount_type', 'discount_value',
                  'max_uses', 'current_uses', 'remaining_uses', 'valid_from',
                  'valid_until', 'min_purchase_amount', 'is_active', 'created_at']
    
    def get_remaining_uses(self, obj):
        return obj.remaining_uses()
