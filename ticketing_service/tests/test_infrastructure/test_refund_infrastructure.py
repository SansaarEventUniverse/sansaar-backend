from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
import uuid

from domain.refund import Refund
from domain.ticket import Ticket
from domain.order import Order
from domain.ticket_type import TicketType
from infrastructure.repositories.refund_repository import (
    RefundRepository,
    RefundProcessor
)


class RefundRepositoryTest(TestCase):
    """Tests for RefundRepository."""
    
    def setUp(self):
        self.repository = RefundRepository()
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
            total_amount=Decimal('100.00'),
            status='confirmed'
        )
        
        self.ticket = Ticket.objects.create(
            ticket_type_id=self.ticket_type.id,
            order_id=self.order.id,
            attendee_name='Test User',
            attendee_email='test@example.com'
        )
        
        self.refund = Refund.objects.create(
            ticket_id=self.ticket.id,
            order_id=self.order.id,
            original_amount=Decimal('50.00'),
            refund_amount=Decimal('40.00'),
            reason='Test'
        )
    
    def test_get_order_refunds(self):
        """Test getting order refunds."""
        refunds = self.repository.get_order_refunds(self.order.id)
        self.assertEqual(len(refunds), 1)
        self.assertEqual(refunds[0].id, self.refund.id)
    
    def test_get_pending_refunds(self):
        """Test getting pending refunds."""
        refunds = self.repository.get_pending_refunds()
        self.assertEqual(len(refunds), 1)
    
    def test_get_refund_analytics(self):
        """Test getting refund analytics."""
        analytics = self.repository.get_refund_analytics()
        
        self.assertEqual(analytics['total_refunds'], 1)
        self.assertEqual(analytics['total_amount'], Decimal('40.00'))
        self.assertEqual(analytics['pending_count'], 1)


class RefundProcessorTest(TestCase):
    """Tests for RefundProcessor."""
    
    def test_calculate_refund_with_policy(self):
        """Test calculating refund with policy."""
        refund = RefundProcessor.calculate_refund_with_policy(
            Decimal('100.00'),
            Decimal('80.00'),
            Decimal('5.00')
        )
        self.assertEqual(refund, Decimal('75.00'))
    
    def test_refund_cannot_be_negative(self):
        """Test refund cannot be negative."""
        refund = RefundProcessor.calculate_refund_with_policy(
            Decimal('10.00'),
            Decimal('50.00'),
            Decimal('10.00')
        )
        self.assertEqual(refund, Decimal('0.00'))
