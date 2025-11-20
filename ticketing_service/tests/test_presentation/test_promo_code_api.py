from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from datetime import timedelta
import uuid

from domain.promo_code import PromoCode
from domain.order import Order, OrderItem
from domain.ticket_type import TicketType


class PromoCodeAPITest(TestCase):
    """Tests for promo code API endpoints."""
    
    def setUp(self):
        self.client = APIClient()
        self.event_id = uuid.uuid4()
        self.now = timezone.now()
    
    def test_create_promo_code(self):
        """Test creating a promo code."""
        data = {
            'code': 'SAVE20',
            'discount_type': 'percentage',
            'discount_value': '20.00',
            'max_uses': 100,
            'valid_from': self.now.isoformat(),
            'valid_until': (self.now + timedelta(days=30)).isoformat()
        }
        
        response = self.client.post(
            f'/api/tickets/events/{self.event_id}/promo-codes/',
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['code'], 'SAVE20')
    
    def test_validate_promo_code(self):
        """Test validating a promo code."""
        promo = PromoCode.objects.create(
            code='SAVE20',
            discount_type='percentage',
            discount_value=Decimal('20.00'),
            max_uses=100,
            valid_from=self.now - timedelta(days=1),
            valid_until=self.now + timedelta(days=30)
        )
        
        data = {
            'code': 'SAVE20',
            'order_amount': '100.00'
        }
        
        response = self.client.post(
            '/api/tickets/promo-codes/validate/',
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['discount_amount'], '20.00')
        self.assertEqual(response.data['final_amount'], '80.00')
    
    def test_apply_promo_code(self):
        """Test applying promo code to order."""
        promo = PromoCode.objects.create(
            code='SAVE20',
            event_id=self.event_id,
            discount_type='percentage',
            discount_value=Decimal('20.00'),
            max_uses=100,
            valid_from=self.now - timedelta(days=1),
            valid_until=self.now + timedelta(days=30)
        )
        
        ticket_type = TicketType.objects.create(
            event_id=self.event_id,
            name='General',
            price=Decimal('50.00'),
            quantity=100,
            sale_start=self.now - timedelta(days=1),
            sale_end=self.now + timedelta(days=30)
        )
        
        order = Order.objects.create(
            user_id=uuid.uuid4(),
            event_id=self.event_id,
            total_amount=Decimal('100.00')
        )
        OrderItem.objects.create(
            order=order,
            ticket_type_id=ticket_type.id,
            quantity=2,
            unit_price=Decimal('50.00')
        )
        
        data = {'promo_code': 'SAVE20'}
        
        response = self.client.post(
            f'/api/tickets/orders/{order.id}/apply-promo/',
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['new_total'], '80.00')
