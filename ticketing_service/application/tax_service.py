import uuid
from decimal import Decimal
from typing import Dict, Any
from django.db.models import Sum, Count

from domain.tax import TaxRule, TaxCalculation
from domain.order import Order


class TaxCalculationService:
    """Service for calculating taxes."""
    
    def calculate_for_order(self, order: Order, country: str = 'US', state: str = '') -> TaxCalculation:
        """Calculate tax for an order."""
        # Get applicable tax rule
        try:
            if state:
                tax_rule = TaxRule.objects.get(country=country, state=state, is_active=True)
            else:
                tax_rule = TaxRule.objects.get(country=country, state='', is_active=True)
        except TaxRule.DoesNotExist:
            # Default to 0% tax if no rule found
            tax_rule = TaxRule(
                name='No Tax',
                country=country,
                tax_rate=Decimal('0.00')
            )
            tax_rule.save()
        
        # Calculate tax
        tax_amount = tax_rule.calculate_tax(order.total_amount)
        
        # Create tax calculation
        calc = TaxCalculation.objects.create(
            order_id=order.id,
            tax_rule_id=tax_rule.id,
            subtotal=order.total_amount,
            tax_amount=tax_amount,
            currency=order.currency
        )
        
        return calc


class TaxComplianceService:
    """Service for tax compliance tracking."""
    
    def check_compliance(self, event_id: uuid.UUID) -> Dict[str, Any]:
        """Check tax compliance for an event."""
        # Get all orders for event
        orders = Order.objects.filter(event_id=event_id, status='confirmed')
        
        # Get tax calculations
        order_ids = orders.values_list('id', flat=True)
        calculations = TaxCalculation.objects.filter(order_id__in=order_ids)
        
        total_orders = orders.count()
        taxed_orders = calculations.count()
        
        compliance_rate = (taxed_orders / total_orders * 100) if total_orders > 0 else 0
        
        return {
            'total_orders': total_orders,
            'taxed_orders': taxed_orders,
            'untaxed_orders': total_orders - taxed_orders,
            'compliance_rate': round(compliance_rate, 2),
            'is_compliant': compliance_rate >= 95.0
        }


class TaxReportingService:
    """Service for tax reporting."""
    
    def generate_report(self, event_id: uuid.UUID) -> Dict[str, Any]:
        """Generate tax report for an event."""
        # Get all orders for event
        orders = Order.objects.filter(event_id=event_id, status='confirmed')
        order_ids = orders.values_list('id', flat=True)
        
        # Get tax calculations
        calculations = TaxCalculation.objects.filter(order_id__in=order_ids)
        
        stats = calculations.aggregate(
            total_subtotal=Sum('subtotal'),
            total_tax=Sum('tax_amount'),
            total_with_tax=Sum('total'),
            total_transactions=Count('id')
        )
        
        return {
            'event_id': event_id,
            'total_subtotal': stats['total_subtotal'] or Decimal('0.00'),
            'total_tax_collected': stats['total_tax'] or Decimal('0.00'),
            'total_with_tax': stats['total_with_tax'] or Decimal('0.00'),
            'total_transactions': stats['total_transactions'] or 0,
            'currency': 'USD'
        }
