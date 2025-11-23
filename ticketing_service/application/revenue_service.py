import uuid
from decimal import Decimal
from typing import Dict, Any
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta

from domain.revenue import Revenue, RevenueReport
from domain.order import Order
from domain.refund import Refund


class RevenueCalculationService:
    """Service for calculating revenue."""
    
    def calculate_from_order(self, order: Order, platform_fee_percent: Decimal = Decimal('10.00')) -> Revenue:
        """Calculate revenue from an order."""
        gross = order.total_amount
        platform_fee = (gross * platform_fee_percent / 100).quantize(Decimal('0.01'))
        payment_fee = (gross * Decimal('2.9') / 100 + Decimal('0.30')).quantize(Decimal('0.01'))
        
        revenue = Revenue.objects.create(
            event_id=order.event_id,
            order_id=order.id,
            gross_amount=gross,
            platform_fee=platform_fee,
            payment_fee=payment_fee,
            currency=order.currency
        )
        
        return revenue


class RevenueReportService:
    """Service for generating revenue reports."""
    
    def generate_report(self, event_id: uuid.UUID, period: str = 'daily') -> RevenueReport:
        """Generate revenue report for an event."""
        now = timezone.now()
        
        if period == 'daily':
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = start_date + timedelta(days=1)
        elif period == 'weekly':
            start_date = now - timedelta(days=now.weekday())
            start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = start_date + timedelta(days=7)
        elif period == 'monthly':
            start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            if now.month == 12:
                end_date = start_date.replace(year=now.year + 1, month=1)
            else:
                end_date = start_date.replace(month=now.month + 1)
        else:
            start_date = now - timedelta(days=30)
            end_date = now
        
        # Get revenue data
        revenues = Revenue.objects.filter(
            event_id=event_id,
            created_at__gte=start_date,
            created_at__lt=end_date
        )
        
        stats = revenues.aggregate(
            total_gross=Sum('gross_amount'),
            total_fees=Sum('platform_fee') + Sum('payment_fee'),
            total_net=Sum('net_amount'),
            total_orders=Count('order_id', distinct=True)
        )
        
        # Get refund data
        refunds = Refund.objects.filter(
            order_id__in=revenues.values_list('order_id', flat=True),
            created_at__gte=start_date,
            created_at__lt=end_date,
            status='completed'
        )
        
        total_refunds = refunds.aggregate(total=Sum('refund_amount'))['total'] or Decimal('0.00')
        
        report = RevenueReport.objects.create(
            event_id=event_id,
            period=period,
            start_date=start_date,
            end_date=end_date,
            total_gross=stats['total_gross'] or Decimal('0.00'),
            total_fees=stats['total_fees'] or Decimal('0.00'),
            total_net=stats['total_net'] or Decimal('0.00'),
            total_orders=stats['total_orders'] or 0,
            total_refunds=total_refunds
        )
        
        return report


class PayoutManagementService:
    """Service for managing payouts."""
    
    def calculate_payout(self, event_id: uuid.UUID) -> Dict[str, Any]:
        """Calculate payout amount for an event."""
        revenues = Revenue.objects.filter(event_id=event_id)
        
        total_net = revenues.aggregate(total=Sum('net_amount'))['total'] or Decimal('0.00')
        
        # Get refunds for orders in this event
        order_ids = revenues.values_list('order_id', flat=True)
        refunds = Refund.objects.filter(
            order_id__in=order_ids,
            status='completed'
        )
        
        total_refunds = refunds.aggregate(total=Sum('refund_amount'))['total'] or Decimal('0.00')
        
        payout_amount = total_net - total_refunds
        
        return {
            'event_id': event_id,
            'total_revenue': total_net,
            'total_refunds': total_refunds,
            'payout_amount': max(Decimal('0.00'), payout_amount),
            'currency': 'USD'
        }
