import uuid
from decimal import Decimal
from typing import Dict, Any
from django.core.exceptions import ValidationError
from django.db import transaction

from domain.refund import Refund, RefundPolicy
from domain.ticket import Ticket
from domain.order import Order


class RefundPolicyService:
    """Service for managing refund policies."""
    
    def get_policy(self, event_id: uuid.UUID) -> RefundPolicy:
        """Get refund policy for event."""
        try:
            return RefundPolicy.objects.get(event_id=event_id)
        except RefundPolicy.DoesNotExist:
            # Return default policy
            return RefundPolicy(
                event_id=event_id,
                refund_allowed=True,
                refund_before_hours=24,
                refund_percentage=Decimal('100.00'),
                processing_fee=Decimal('0.00')
            )


class CancelTicketService:
    """Service for cancelling tickets."""
    
    def execute(self, ticket_id: uuid.UUID, reason: str) -> Ticket:
        """Cancel a ticket."""
        try:
            ticket = Ticket.objects.get(id=ticket_id)
        except Ticket.DoesNotExist:
            raise ValidationError("Ticket not found")
        
        if ticket.status != 'active':
            raise ValidationError("Only active tickets can be cancelled")
        
        ticket.cancel()
        return ticket


class ProcessRefundService:
    """Service for processing refunds."""
    
    def execute(self, data: Dict[str, Any]) -> Refund:
        """Process a refund request."""
        try:
            ticket = Ticket.objects.get(id=data['ticket_id'])
        except Ticket.DoesNotExist:
            raise ValidationError("Ticket not found")
        
        try:
            order = Order.objects.get(id=ticket.order_id)
        except Order.DoesNotExist:
            raise ValidationError("Order not found")
        
        if ticket.status == 'cancelled':
            raise ValidationError("Ticket is already cancelled")
        
        # Get refund policy
        policy_service = RefundPolicyService()
        policy = policy_service.get_policy(order.event_id)
        
        if not policy.refund_allowed:
            raise ValidationError("Refunds are not allowed for this event")
        
        # Calculate refund amount
        original_amount = data.get('original_amount', Decimal('0.00'))
        
        with transaction.atomic():
            # Create refund
            refund = Refund.objects.create(
                ticket_id=ticket.id,
                order_id=order.id,
                payment_id=order.payment_id,
                original_amount=original_amount,
                refund_amount=Decimal('0.00'),
                processing_fee=policy.processing_fee,
                reason=data.get('reason', 'Customer request')
            )
            
            # Calculate refund amount based on policy
            refund.refund_amount = refund.calculate_refund(policy)
            refund.save()
            
            # Cancel ticket
            cancel_service = CancelTicketService()
            cancel_service.execute(ticket.id, data.get('reason', 'Refund requested'))
            
            return refund
