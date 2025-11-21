import uuid
from typing import List, Dict, Any
from decimal import Decimal
from django.db.models import Sum, Count, Q
from django.utils import timezone

from domain.promo_code import PromoCode


class PromoCodeRepository:
    """Repository for promo code data access."""
    
    def get_active_codes(self, event_id: uuid.UUID = None) -> List[PromoCode]:
        """Get all active promo codes."""
        now = timezone.now()
        queryset = PromoCode.objects.filter(
            is_active=True,
            valid_from__lte=now,
            valid_until__gte=now
        )
        
        if event_id:
            queryset = queryset.filter(Q(event_id=event_id) | Q(event_id__isnull=True))
        
        return list(queryset.order_by('-created_at'))
    
    def get_analytics(self, promo_code_id: uuid.UUID) -> Dict[str, Any]:
        """Get analytics for a promo code."""
        try:
            promo = PromoCode.objects.get(id=promo_code_id)
        except PromoCode.DoesNotExist:
            return {}
        
        usage_rate = 0
        if promo.max_uses > 0:
            usage_rate = (promo.current_uses / promo.max_uses) * 100
        
        return {
            'code': promo.code,
            'total_uses': promo.current_uses,
            'remaining_uses': promo.remaining_uses(),
            'usage_rate': usage_rate,
            'is_active': promo.is_active,
            'is_valid': promo.is_valid()
        }


class DiscountCalculator:
    """Utility for discount calculations."""
    
    @staticmethod
    def calculate_percentage_discount(amount: Decimal, percentage: Decimal) -> Decimal:
        """Calculate percentage discount."""
        return (amount * percentage / 100).quantize(Decimal('0.01'))
    
    @staticmethod
    def calculate_fixed_discount(amount: Decimal, fixed_amount: Decimal) -> Decimal:
        """Calculate fixed discount."""
        return min(fixed_amount, amount)
    
    @staticmethod
    def apply_discount(amount: Decimal, discount_type: str, discount_value: Decimal) -> Decimal:
        """Apply discount and return final amount."""
        if discount_type == 'percentage':
            discount = DiscountCalculator.calculate_percentage_discount(amount, discount_value)
        else:
            discount = DiscountCalculator.calculate_fixed_discount(amount, discount_value)
        
        return amount - discount
