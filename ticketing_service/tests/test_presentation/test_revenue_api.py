from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient
import uuid

from domain.revenue import Revenue
from domain.order import Order


class RevenueAPITest(TestCase):
    """Tests for revenue API endpoints."""
    
    def setUp(self):
        self.client = APIClient()
        self.event_id = uuid.uuid4()
        
        order = Order.objects.create(
            user_id=uuid.uuid4(),
            event_id=self.event_id,
            total_amount=Decimal('100.00'),
            status='confirmed'
        )
        
        Revenue.objects.create(
            event_id=self.event_id,
            order_id=order.id,
            gross_amount=Decimal('100.00'),
            platform_fee=Decimal('10.00'),
            payment_fee=Decimal('3.00')
        )
    
    def test_get_revenue(self):
        """Test getting event revenue."""
        response = self.client.get(f'/api/tickets/events/{self.event_id}/revenue/')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('revenues', response.data)
        self.assertIn('analytics', response.data)
        self.assertEqual(len(response.data['revenues']), 1)
    
    def test_generate_report(self):
        """Test generating revenue report."""
        response = self.client.get(
            f'/api/tickets/events/{self.event_id}/revenue/report/',
            {'period': 'daily'}
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['period'], 'daily')
        self.assertEqual(response.data['total_gross'], '100.00')
    
    def test_process_payout(self):
        """Test processing payout."""
        response = self.client.post(f'/api/tickets/events/{self.event_id}/payout/')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('payout', response.data)
        self.assertEqual(response.data['payout']['total_revenue'], '87.00')
