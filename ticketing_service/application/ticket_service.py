import uuid
from typing import Dict, Any, List
from django.core.exceptions import ValidationError
from domain.ticket import Ticket


class GenerateTicketService:
    """Service for generating tickets."""
    
    def execute(self, data: Dict[str, Any]) -> Ticket:
        """Generate a new ticket."""
        ticket = Ticket.objects.create(
            ticket_type_id=data['ticket_type_id'],
            order_id=data['order_id'],
            attendee_name=data['attendee_name'],
            attendee_email=data['attendee_email']
        )
        return ticket
    
    def bulk_generate(self, data: Dict[str, Any], quantity: int) -> List[Ticket]:
        """Generate multiple tickets."""
        tickets = []
        for _ in range(quantity):
            ticket = self.execute(data)
            tickets.append(ticket)
        return tickets


class ValidateQRCodeService:
    """Service for validating QR codes."""
    
    def execute(self, qr_code_data: str) -> Dict[str, Any]:
        """Validate QR code and return ticket info."""
        try:
            ticket = Ticket.objects.get(qr_code_data=qr_code_data)
        except Ticket.DoesNotExist:
            raise ValidationError("Invalid QR code")
        
        return {
            'valid': ticket.is_valid(),
            'ticket_id': str(ticket.id),
            'status': ticket.status,
            'attendee_name': ticket.attendee_name,
            'checked_in': ticket.checked_in_at is not None,
            'checked_in_at': ticket.checked_in_at,
        }


class TicketCheckInService:
    """Service for checking in tickets."""
    
    def execute(self, ticket_id: uuid.UUID, checked_in_by: uuid.UUID) -> Ticket:
        """Check in a ticket."""
        try:
            ticket = Ticket.objects.get(id=ticket_id)
        except Ticket.DoesNotExist:
            raise ValidationError("Ticket not found")
        
        ticket.check_in(checked_in_by)
        return ticket
    
    def check_in_by_qr(self, qr_code_data: str, checked_in_by: uuid.UUID) -> Ticket:
        """Check in ticket using QR code."""
        try:
            ticket = Ticket.objects.get(qr_code_data=qr_code_data)
        except Ticket.DoesNotExist:
            raise ValidationError("Invalid QR code")
        
        ticket.check_in(checked_in_by)
        return ticket
