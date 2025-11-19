import uuid
from decimal import Decimal
from typing import Dict, Any, List
from django.core.exceptions import ValidationError
from django.db import transaction

from domain.order import Order, OrderItem
from domain.ticket_type import TicketType
from domain.ticket import Ticket


class CreateOrderService:
    """Service for creating orders."""
    
    def execute(self, data: Dict[str, Any]) -> Order:
        """Create a new order with items."""
        with transaction.atomic():
            order = Order.objects.create(
                user_id=data['user_id'],
                event_id=data['event_id'],
                total_amount=Decimal('0.00'),
                currency=data.get('currency', 'USD')
            )
            
            for item_data in data['items']:
                ticket_type = TicketType.objects.get(id=item_data['ticket_type_id'])
                
                if not ticket_type.can_purchase(item_data['quantity']):
                    raise ValidationError(f"Cannot purchase {item_data['quantity']} tickets for {ticket_type.name}")
                
                OrderItem.objects.create(
                    order=order,
                    ticket_type_id=ticket_type.id,
                    quantity=item_data['quantity'],
                    unit_price=ticket_type.price
                )
            
            order.calculate_total()
            return order


class ProcessTicketPurchaseService:
    """Service for processing ticket purchases."""
    
    def execute(self, order_id: uuid.UUID, payment_id: uuid.UUID) -> List[Ticket]:
        """Process purchase and generate tickets."""
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            raise ValidationError("Order not found")
        
        if not order.can_purchase():
            raise ValidationError("Order cannot be purchased")
        
        with transaction.atomic():
            # Reserve inventory and generate tickets
            tickets = []
            for item in order.items.all():
                ticket_type = TicketType.objects.get(id=item.ticket_type_id)
                ticket_type.reserve_tickets(item.quantity)
                
                # Generate tickets
                for _ in range(item.quantity):
                    ticket = Ticket.objects.create(
                        ticket_type_id=ticket_type.id,
                        order_id=order.id,
                        attendee_name=f"Attendee",  # Will be updated later
                        attendee_email="temp@example.com"
                    )
                    tickets.append(ticket)
            
            order.confirm(payment_id)
            return tickets


class OrderManagementService:
    """Service for managing orders."""
    
    def get_order(self, order_id: uuid.UUID) -> Order:
        """Get order by ID."""
        try:
            return Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            raise ValidationError("Order not found")
    
    def cancel_order(self, order_id: uuid.UUID) -> Order:
        """Cancel an order and release inventory."""
        order = self.get_order(order_id)
        
        with transaction.atomic():
            # Only release inventory if order was confirmed
            if order.status == 'confirmed':
                for item in order.items.all():
                    ticket_type = TicketType.objects.get(id=item.ticket_type_id)
                    ticket_type.release_tickets(item.quantity)
            
            order.cancel()
            return order
