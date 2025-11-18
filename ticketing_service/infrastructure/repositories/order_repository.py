import uuid
from typing import Dict, Any, List
from django.db.models import Sum, Count, Q
from django.utils import timezone

from domain.order import Order, OrderItem


class OrderRepository:
    """Repository for order data access."""
    
    def get_user_orders(self, user_id: uuid.UUID) -> List[Order]:
        """Get all orders for a user."""
        return list(Order.objects.filter(user_id=user_id).order_by('-created_at'))
    
    def get_event_orders(self, event_id: uuid.UUID) -> List[Order]:
        """Get all orders for an event."""
        return list(Order.objects.filter(event_id=event_id).order_by('-created_at'))
    
    def get_order_analytics(self, event_id: uuid.UUID) -> Dict[str, Any]:
        """Get order analytics for an event."""
        orders = Order.objects.filter(event_id=event_id)
        
        total_revenue = orders.filter(status='confirmed').aggregate(
            total=Sum('total_amount')
        )['total'] or 0
        
        order_stats = orders.aggregate(
            total_orders=Count('id'),
            confirmed_orders=Count('id', filter=Q(status='confirmed')),
            pending_orders=Count('id', filter=Q(status='pending')),
            cancelled_orders=Count('id', filter=Q(status='cancelled'))
        )
        
        return {
            'total_revenue': total_revenue,
            'total_orders': order_stats['total_orders'],
            'confirmed_orders': order_stats['confirmed_orders'],
            'pending_orders': order_stats['pending_orders'],
            'cancelled_orders': order_stats['cancelled_orders']
        }


class InventoryReservationService:
    """Service for managing inventory reservations."""
    
    def __init__(self):
        self.reservations = {}  # In-memory for now, could use Redis
    
    def create_reservation(self, order_id: uuid.UUID, items: List[Dict[str, Any]]) -> str:
        """Create a temporary reservation."""
        reservation_id = str(uuid.uuid4())
        self.reservations[reservation_id] = {
            'order_id': order_id,
            'items': items,
            'created_at': timezone.now()
        }
        return reservation_id
    
    def confirm_reservation(self, reservation_id: str) -> bool:
        """Confirm a reservation."""
        if reservation_id in self.reservations:
            del self.reservations[reservation_id]
            return True
        return False
    
    def release_reservation(self, reservation_id: str) -> bool:
        """Release a reservation."""
        if reservation_id in self.reservations:
            del self.reservations[reservation_id]
            return True
        return False
