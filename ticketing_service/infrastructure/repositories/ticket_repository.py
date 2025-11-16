import uuid
from typing import List
from django.db import models
from domain.ticket import Ticket


class TicketRepository:
    """Repository for ticket queries."""
    
    def get_by_order(self, order_id: uuid.UUID) -> List[Ticket]:
        """Get all tickets for an order."""
        return list(Ticket.objects.filter(order_id=order_id))
    
    def get_active_tickets(self, order_id: uuid.UUID) -> List[Ticket]:
        """Get active tickets for an order."""
        return list(Ticket.objects.filter(order_id=order_id, status='active'))
    
    def get_checked_in_count(self, ticket_type_id: uuid.UUID) -> int:
        """Get count of checked-in tickets for a ticket type."""
        return Ticket.objects.filter(
            ticket_type_id=ticket_type_id,
            status='used'
        ).count()
