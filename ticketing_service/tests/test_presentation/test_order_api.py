from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from datetime import timedelta
import uuid
import json

from domain.ticket_type import TicketType
from domain.order import Order


class OrderAPITest(TestCase):
    """Tests for order API endpoints."""
    
    def setUp(self):
        self.client = APIClient()
        self.event_id = uuid.uuid4()
        self.user_id = uuid.uuid4()
        now = timezone.now()
        
        self.ticket_type = TicketType.objects.create(
            event_id=self.event_id,
            name="General Admission",
            price=Decimal('50.00'),
            quantity=100,
            sale_start=now - timedelta(days=1),
            sale_end=now + timedelta(days=30)
        )
    
    def test_create_order(self):
        """Test creating an order."""
        data = {
            'user_id': str(self.user_id),
            'event_id': str(self.event_id),
            'items': [
                {'ticket_type_id': str(self.ticket_type.id), 'quantity': 2}
            ]
        }
        response = self.client.post('/api/tickets/orders/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['total_amount'], '100.00')
    
    def test_get_order(self):
        """Test getting an order."""
        order = Order.objects.create(
            user_id=self.user_id,
            event_id=self.event_id,
            total_amount=Decimal('100.00')
        )
        response = self.client.get(f'/api/tickets/orders/{order.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], str(order.id))
    
    def test_process_purchase(self):
        """Test processing a purchase."""
        # Create order first
        data = {
            'user_id': str(self.user_id),
            'event_id': str(self.event_id),
            'items': [
                {'ticket_type_id': str(self.ticket_type.id), 'quantity': 2}
            ]
        }
        create_response = self.client.post('/api/tickets/orders/', data, format='json')
        order_id = create_response.data['id']
        
        # Process purchase
        purchase_data = {'payment_id': str(uuid.uuid4())}
        response = self.client.post(
            f'/api/tickets/orders/{order_id}/purchase/',
            purchase_data,
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['tickets_generated'], 2)
