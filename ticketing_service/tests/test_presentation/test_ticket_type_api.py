from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
import uuid
import json

from domain.ticket_type import TicketType


class TicketTypeAPITest(TestCase):
    """Tests for ticket type API endpoints."""
    
    def setUp(self):
        self.event_id = uuid.uuid4()
        self.now = timezone.now()
    
    def test_create_ticket_type(self):
        """Test creating a ticket type via API."""
        data = {
            'name': 'VIP',
            'price': '100.00',
            'quantity': 50,
            'sale_start': (self.now).isoformat(),
            'sale_end': (self.now + timedelta(days=30)).isoformat()
        }
        response = self.client.post(
            f'/api/tickets/events/{self.event_id}/ticket-types/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['name'], 'VIP')
    
    def test_create_ticket_type_invalid_data(self):
        """Test creating ticket type with invalid data."""
        data = {
            'name': 'Test',
            'price': '-10.00',
            'quantity': 50,
            'sale_start': self.now.isoformat(),
            'sale_end': (self.now + timedelta(days=30)).isoformat()
        }
        response = self.client.post(
            f'/api/tickets/events/{self.event_id}/ticket-types/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
    
    def test_update_ticket_type(self):
        """Test updating a ticket type."""
        ticket_type = TicketType.objects.create(
            event_id=self.event_id,
            name='General',
            price=Decimal('50.00'),
            quantity=100,
            sale_start=self.now,
            sale_end=self.now + timedelta(days=30)
        )
        data = {'name': 'General Admission', 'price': '60.00'}
        response = self.client.put(
            f'/api/tickets/ticket-types/{ticket_type.id}/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'General Admission')
    
    def test_get_ticket_types(self):
        """Test getting ticket types for an event."""
        TicketType.objects.create(
            event_id=self.event_id,
            name='VIP',
            price=Decimal('100.00'),
            quantity=50,
            sale_start=self.now,
            sale_end=self.now + timedelta(days=30)
        )
        TicketType.objects.create(
            event_id=self.event_id,
            name='General',
            price=Decimal('50.00'),
            quantity=100,
            sale_start=self.now,
            sale_end=self.now + timedelta(days=30)
        )
        response = self.client.get(f'/api/tickets/events/{self.event_id}/ticket-types/list/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
    
    def test_get_ticket_types_invalid_event_id(self):
        """Test getting ticket types with invalid event ID."""
        response = self.client.get('/api/tickets/events/invalid-id/ticket-types/list/')
        self.assertEqual(response.status_code, 400)
