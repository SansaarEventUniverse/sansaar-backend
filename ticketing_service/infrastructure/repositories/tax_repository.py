import uuid
from typing import List, Dict, Any
from decimal import Decimal
from django.db.models import Sum, Avg

from domain.tax import TaxRule, TaxCalculation


class TaxRepository:
    """Repository for tax data access."""
    
    def get_active_rules(self, country: str = None) -> List[TaxRule]:
        """Get active tax rules."""
        queryset = TaxRule.objects.filter(is_active=True)
        
        if country:
            queryset = queryset.filter(country=country)
        
        return list(queryset.order_by('country', 'state'))
    
    def get_tax_analytics(self, event_id: uuid.UUID = None) -> Dict[str, Any]:
        """Get tax analytics."""
        queryset = TaxCalculation.objects.all()
        
        stats = queryset.aggregate(
            total_tax_collected=Sum('tax_amount'),
            avg_tax_amount=Avg('tax_amount'),
            total_transactions=Sum('id')
        )
        
        return {
            'total_tax_collected': stats['total_tax_collected'] or Decimal('0.00'),
            'avg_tax_amount': stats['avg_tax_amount'] or Decimal('0.00'),
            'total_transactions': queryset.count()
        }


class TaxCalculationEngine:
    """Utility for tax calculations."""
    
    @staticmethod
    def calculate_with_rule(amount: Decimal, tax_rule: TaxRule) -> Dict[str, Decimal]:
        """Calculate tax with a specific rule."""
        tax_amount = tax_rule.calculate_tax(amount)
        total = amount + tax_amount
        
        return {
            'subtotal': amount,
            'tax_amount': tax_amount,
            'total': total,
            'tax_rate': tax_rule.tax_rate
        }
    
    @staticmethod
    def calculate_reverse_tax(total_with_tax: Decimal, tax_rate: Decimal) -> Dict[str, Decimal]:
        """Calculate original amount from total with tax."""
        subtotal = (total_with_tax / (1 + tax_rate / 100)).quantize(Decimal('0.01'))
        tax_amount = total_with_tax - subtotal
        
        return {
            'subtotal': subtotal,
            'tax_amount': tax_amount,
            'total': total_with_tax
        }
