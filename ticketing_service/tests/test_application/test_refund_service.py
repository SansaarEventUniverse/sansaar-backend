from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
import uuid

from domain.refund import Refund, RefundPolicy
from domain.ticket import Ticket
from domain.order import Order, OrderItem
from domain.ticket_type import TicketType
from application.refund_service import (
    RefundPolicyService,
    CancelTicketService,
    ProcessRefundService
)


class RefundPolicyServiceTest(TestCase):
    """Tests for RefundPolicyService."""
    
    def setUp(self):
        self.service = RefundPolicyService()
        self.event_id = uuid.uuid4()
    
    def test_get_existing_policy(self):
        """Test getting existing policy."""
        policy = RefundPolicy.objects.create(
            event_id=self.event_id,
            refund_percentage=Decimal('80.00')
        )
        
        result = self.service.get_policy(self.event_id)
        self.assertEqual(result.id, policy.id)
    
    def test_get_default_policy(self):
        """Test getting default policy when none exists."""
        result = self.service.get_policy(uuid.uuid4())
        self.assertEqual(result.refund_percentage, Decimal('100.00'))


class CancelTicketServiceTest(TestCase):
    """Tests for CancelTicketService."""
    
    def setUp(self):
        self.service = CancelTicketService()
        self.event_id = uuid.uuid4()
        now = timezone.now()
        
        self.ticket_type = TicketType.objects.create(
            event_id=self.event_id,
            name='General',
            price=Decimal('50.00'),
            quantity=100,
            sale_start=now - timedelta(days=1),
            sale_end=now + timedelta(days=30)
        )
        
        self.order = Order.objects.create(
            user_id=uuid.uuid4(),
            event_id=self.event_id,
            total_amount=Decimal('50.00'),
            status='confirmed'
        )
        
        self.ticket = Ticket.objects.create(
            ticket_type_id=self.ticket_type.id,
            order_id=self.order.id,
            attendee_name='Test User',
            attendee_email='test@example.com'
        )
    
    def test_cancel_ticket(self):
        """Test cancelling a ticket."""
        ticket = self.service.execute(self.ticket.id, 'Customer request')
        self.assertEqual(ticket.status, 'cancelled')
    
    def test_cannot_cancel_non_active(self):
        """Test cannot cancel non-active ticket."""
        self.ticket.status = 'used'
        self.ticket.save()
        
        with self.assertRaises(ValidationError):
            self.service.execute(self.ticket.id, 'Test')


class ProcessRefundServiceTest(TestCase):
    """Tests for ProcessRefundService."""
    
    def setUp(self):
        self.service = ProcessRefundService()
        self.event_id = uuid.uuid4()
        now = timezone.now()
        
        self.policy = RefundPolicy.objects.create(
            event_id=self.event_id,
            refund_percentage=Decimal('80.00'),
            processing_fee=Decimal('5.00')
        )
        
        self.ticket_type = TicketType.objects.create(
            event_id=self.event_id,
            name='General',
            price=Decimal('50.00'),
            quantity=100,
            sale_start=now - timedelta(days=1),
            sale_end=now + timedelta(days=30)
        )
        
        self.order = Order.objects.create(
            user_id=uuid.uuid4(),
            event_id=self.event_id,
            total_amount=Decimal('50.00'),
            status='confirmed'
        )
        
        self.ticket = Ticket.objects.create(
            ticket_type_id=self.ticket_type.id,
            order_id=self.order.id,
            attendee_name='Test User',
            attendee_email='test@example.com'
        )
    
    def test_process_refund(self):
        """Test processing a refund."""
        data = {
            'ticket_id': self.ticket.id,
            'original_amount': Decimal('50.00'),
            'reason': 'Customer request'
        }
        
        refund = self.service.execute(data)
        
        self.assertEqual(refund.status, 'pending')
        self.assertEqual(refund.refund_amount, Decimal('35.00'))  # 50 * 0.8 - 5
        
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.status, 'cancelled')
    
    def test_cannot_refund_cancelled_ticket(self):
        """Test cannot refund already cancelled ticket."""
        self.ticket.cancel()
        
        data = {
            'ticket_id': self.ticket.id,
            'original_amount': Decimal('50.00')
        }
        
        with self.assertRaises(ValidationError):
            self.service.execute(data)
