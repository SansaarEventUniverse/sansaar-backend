import uuid
from typing import List, Dict, Any
from decimal import Decimal
from django.db.models import Sum, Count, Q

from domain.refund import Refund


class RefundRepository:
    """Repository for refund data access."""
    
    def get_order_refunds(self, order_id: uuid.UUID) -> List[Refund]:
        """Get all refunds for an order."""
        return list(Refund.objects.filter(order_id=order_id).order_by('-created_at'))
    
    def get_pending_refunds(self) -> List[Refund]:
        """Get all pending refunds."""
        return list(Refund.objects.filter(status='pending').order_by('created_at'))
    
    def get_refund_analytics(self, event_id: uuid.UUID = None) -> Dict[str, Any]:
        """Get refund analytics."""
        queryset = Refund.objects.all()
        
        stats = queryset.aggregate(
            total_refunds=Count('id'),
            total_amount=Sum('refund_amount'),
            pending_count=Count('id', filter=Q(status='pending')),
            completed_count=Count('id', filter=Q(status='completed')),
            rejected_count=Count('id', filter=Q(status='rejected'))
        )
        
        return {
            'total_refunds': stats['total_refunds'] or 0,
            'total_amount': stats['total_amount'] or Decimal('0.00'),
            'pending_count': stats['pending_count'] or 0,
            'completed_count': stats['completed_count'] or 0,
            'rejected_count': stats['rejected_count'] or 0
        }


class RefundProcessor:
    """Utility for processing refunds."""
    
    @staticmethod
    def calculate_refund_with_policy(amount: Decimal, percentage: Decimal, fee: Decimal) -> Decimal:
        """Calculate refund amount with policy."""
        refund = (amount * percentage / 100) - fee
        return max(Decimal('0.00'), refund).quantize(Decimal('0.01'))
