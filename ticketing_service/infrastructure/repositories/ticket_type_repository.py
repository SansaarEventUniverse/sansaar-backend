import uuid
from typing import List
from django.db import models
from domain.ticket_type import TicketType


class TicketTypeRepository:
    """Repository for complex ticket type queries."""
    
    def get_by_event(self, event_id: uuid.UUID, active_only: bool = True) -> List[TicketType]:
        """Get all ticket types for an event."""
        queryset = TicketType.objects.filter(event_id=event_id)
        if active_only:
            queryset = queryset.filter(is_active=True)
        return list(queryset.order_by('price'))
    
    def get_available_types(self, event_id: uuid.UUID) -> List[TicketType]:
        """Get available ticket types for an event."""
        from django.utils import timezone
        now = timezone.now()
        return list(
            TicketType.objects.filter(
                event_id=event_id,
                is_active=True,
                sale_start__lte=now,
                sale_end__gte=now
            ).exclude(
                quantity_sold__gte=models.F('quantity')
            ).order_by('price')
        )
