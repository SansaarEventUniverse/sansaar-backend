from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from datetime import timedelta
import uuid

from domain.refund import Refund, RefundPolicy
from domain.ticket import Ticket
from domain.order import Order
from domain.ticket_type import TicketType


class RefundAPITest(TestCase):
    """Tests for refund API endpoints."""
    
    def setUp(self):
        self.client = APIClient()
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
    
    def test_request_refund(self):
        """Test requesting a refund."""
        data = {
            'ticket_id': str(self.ticket.id),
            'original_amount': '50.00',
            'reason': 'Customer request'
        }
        
        response = self.client.post(
            '/api/tickets/refunds/request/',
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['status'], 'pending')
        self.assertEqual(response.data['refund_amount'], '35.00')  # 50 * 0.8 - 5
    
    def test_get_refund_status(self):
        """Test getting refund status."""
        refund = Refund.objects.create(
            ticket_id=self.ticket.id,
            order_id=self.order.id,
            original_amount=Decimal('50.00'),
            refund_amount=Decimal('35.00'),
            reason='Test'
        )
        
        response = self.client.get(f'/api/tickets/refunds/{refund.id}/')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], str(refund.id))
        self.assertEqual(response.data['status'], 'pending')
    
    def test_process_refund_approve(self):
        """Test approving a refund."""
        refund = Refund.objects.create(
            ticket_id=self.ticket.id,
            order_id=self.order.id,
            original_amount=Decimal('50.00'),
            refund_amount=Decimal('35.00'),
            reason='Test'
        )
        
        data = {'action': 'approve'}
        
        response = self.client.post(
            f'/api/tickets/refunds/{refund.id}/process/',
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['refund']['status'], 'completed')
    
    def test_process_refund_reject(self):
        """Test rejecting a refund."""
        refund = Refund.objects.create(
            ticket_id=self.ticket.id,
            order_id=self.order.id,
            original_amount=Decimal('50.00'),
            refund_amount=Decimal('35.00'),
            reason='Test'
        )
        
        data = {
            'action': 'reject',
            'rejection_reason': 'Policy violation'
        }
        
        response = self.client.post(
            f'/api/tickets/refunds/{refund.id}/process/',
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['refund']['status'], 'rejected')
