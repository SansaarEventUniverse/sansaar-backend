import uuid
from typing import Dict, Any
from django.core.exceptions import ValidationError
from domain.ticket_type import TicketType


class CreateTicketTypeService:
    """Service for creating ticket types."""
    
    def execute(self, data: Dict[str, Any]) -> TicketType:
        """Create a new ticket type."""
        ticket_type = TicketType(
            event_id=data['event_id'],
            name=data['name'],
            description=data.get('description', ''),
            price=data['price'],
            currency=data.get('currency', 'USD'),
            quantity=data['quantity'],
            min_purchase=data.get('min_purchase', 1),
            max_purchase=data.get('max_purchase', 10),
            sale_start=data['sale_start'],
            sale_end=data['sale_end'],
        )
        ticket_type.clean()
        ticket_type.save()
        return ticket_type


class UpdateTicketTypeService:
    """Service for updating ticket types."""
    
    def execute(self, ticket_type_id: uuid.UUID, data: Dict[str, Any]) -> TicketType:
        """Update an existing ticket type."""
        try:
            ticket_type = TicketType.objects.get(id=ticket_type_id)
        except TicketType.DoesNotExist:
            raise ValidationError("Ticket type not found")
        
        # Update fields
        for field in ['name', 'description', 'price', 'quantity', 'min_purchase', 'max_purchase', 'sale_start', 'sale_end', 'is_active']:
            if field in data:
                setattr(ticket_type, field, data[field])
        
        ticket_type.clean()
        ticket_type.save()
        return ticket_type


class ManageTicketInventoryService:
    """Service for managing ticket inventory."""
    
    def reserve_tickets(self, ticket_type_id: uuid.UUID, quantity: int) -> TicketType:
        """Reserve tickets from inventory."""
        try:
            ticket_type = TicketType.objects.get(id=ticket_type_id)
        except TicketType.DoesNotExist:
            raise ValidationError("Ticket type not found")
        
        ticket_type.reserve_tickets(quantity)
        return ticket_type
    
    def release_tickets(self, ticket_type_id: uuid.UUID, quantity: int) -> TicketType:
        """Release tickets back to inventory."""
        try:
            ticket_type = TicketType.objects.get(id=ticket_type_id)
        except TicketType.DoesNotExist:
            raise ValidationError("Ticket type not found")
        
        ticket_type.release_tickets(quantity)
        return ticket_type
    
    def get_availability(self, ticket_type_id: uuid.UUID) -> Dict[str, Any]:
        """Get ticket availability information."""
        try:
            ticket_type = TicketType.objects.get(id=ticket_type_id)
        except TicketType.DoesNotExist:
            raise ValidationError("Ticket type not found")
        
        return {
            'ticket_type_id': str(ticket_type.id),
            'total_quantity': ticket_type.quantity,
            'quantity_sold': ticket_type.quantity_sold,
            'available_quantity': ticket_type.available_quantity(),
            'is_available': ticket_type.is_available(),
        }
