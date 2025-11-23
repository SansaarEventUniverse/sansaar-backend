import uuid
from typing import List, Dict, Any
from decimal import Decimal
from django.db.models import Sum, Avg, Count, Q
from django.utils import timezone
from datetime import timedelta

from domain.revenue import Revenue, RevenueReport


class RevenueRepository:
    """Repository for revenue data access."""
    
    def get_event_revenue(self, event_id: uuid.UUID) -> List[Revenue]:
        """Get all revenue for an event."""
        return list(Revenue.objects.filter(event_id=event_id).order_by('-created_at'))
    
    def get_revenue_analytics(self, event_id: uuid.UUID) -> Dict[str, Any]:
        """Get revenue analytics for an event."""
        revenues = Revenue.objects.filter(event_id=event_id)
        
        stats = revenues.aggregate(
            total_gross=Sum('gross_amount'),
            total_platform_fees=Sum('platform_fee'),
            total_payment_fees=Sum('payment_fee'),
            total_net=Sum('net_amount'),
            avg_order_value=Avg('gross_amount'),
            total_orders=Count('order_id', distinct=True)
        )
        
        return {
            'total_gross': stats['total_gross'] or Decimal('0.00'),
            'total_platform_fees': stats['total_platform_fees'] or Decimal('0.00'),
            'total_payment_fees': stats['total_payment_fees'] or Decimal('0.00'),
            'total_net': stats['total_net'] or Decimal('0.00'),
            'avg_order_value': stats['avg_order_value'] or Decimal('0.00'),
            'total_orders': stats['total_orders'] or 0
        }
    
    def get_recent_reports(self, event_id: uuid.UUID, limit: int = 10) -> List[RevenueReport]:
        """Get recent revenue reports."""
        return list(RevenueReport.objects.filter(event_id=event_id).order_by('-created_at')[:limit])


class RevenueTracker:
    """Utility for tracking revenue in real-time."""
    
    @staticmethod
    def track_order_revenue(event_id: uuid.UUID, order_id: uuid.UUID, amount: Decimal) -> Revenue:
        """Track revenue from an order."""
        platform_fee = (amount * Decimal('10.00') / 100).quantize(Decimal('0.01'))
        payment_fee = (amount * Decimal('2.9') / 100 + Decimal('0.30')).quantize(Decimal('0.01'))
        
        return Revenue.objects.create(
            event_id=event_id,
            order_id=order_id,
            gross_amount=amount,
            platform_fee=platform_fee,
            payment_fee=payment_fee
        )
