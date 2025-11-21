import uuid
from decimal import Decimal
from typing import Dict, Any
from django.core.exceptions import ValidationError
from django.utils import timezone

from domain.promo_code import PromoCode
from domain.order import Order


class CreatePromoCodeService:
    """Service for creating promo codes."""
    
    def execute(self, data: Dict[str, Any]) -> PromoCode:
        """Create a new promo code."""
        promo = PromoCode.objects.create(
            code=data['code'].upper(),
            event_id=data.get('event_id'),
            discount_type=data['discount_type'],
            discount_value=data['discount_value'],
            max_uses=data.get('max_uses', 0),
            valid_from=data['valid_from'],
            valid_until=data['valid_until'],
            min_purchase_amount=data.get('min_purchase_amount', Decimal('0.00'))
        )
        promo.clean()
        return promo


class ValidatePromoCodeService:
    """Service for validating promo codes."""
    
    def execute(self, code: str, order_amount: Decimal, event_id: uuid.UUID = None) -> Dict[str, Any]:
        """Validate promo code and return discount info."""
        try:
            promo = PromoCode.objects.get(code=code.upper())
        except PromoCode.DoesNotExist:
            raise ValidationError("Promo code not found")
        
        if event_id and promo.event_id and promo.event_id != event_id:
            raise ValidationError("Promo code not valid for this event")
        
        if not promo.can_apply(order_amount):
            if not promo.is_valid():
                raise ValidationError("Promo code is expired or inactive")
            raise ValidationError(f"Minimum purchase amount is {promo.min_purchase_amount}")
        
        discount = promo.calculate_discount(order_amount)
        
        return {
            'promo_code': promo,
            'discount_amount': discount,
            'final_amount': order_amount - discount,
            'discount_type': promo.discount_type,
            'discount_value': promo.discount_value
        }


class ApplyDiscountService:
    """Service for applying discounts to orders."""
    
    def execute(self, order_id: uuid.UUID, promo_code: str) -> Order:
        """Apply promo code discount to order."""
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            raise ValidationError("Order not found")
        
        if order.status != 'pending':
            raise ValidationError("Can only apply promo codes to pending orders")
        
        validator = ValidatePromoCodeService()
        result = validator.execute(promo_code, order.total_amount, order.event_id)
        
        promo = result['promo_code']
        promo.apply()
        
        # Update order with discount
        order.total_amount = result['final_amount']
        order.save()
        
        return order
