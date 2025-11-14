from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
import uuid

from domain.ticket_type import TicketType
from application.ticket_type_service import (
    CreateTicketTypeService,
    UpdateTicketTypeService,
    ManageTicketInventoryService
)


class CreateTicketTypeServiceTest(TestCase):
    """Tests for CreateTicketTypeService."""
    
    def setUp(self):
        self.service = CreateTicketTypeService()
        self.event_id = uuid.uuid4()
        self.now = timezone.now()
    
    def test_create_ticket_type(self):
        """Test creating a ticket type."""
        data = {
            'event_id': self.event_id,
            'name': 'VIP',
            'price': Decimal('100.00'),
            'quantity': 50,
            'sale_start': self.now,
            'sale_end': self.now + timedelta(days=30)
        }
        ticket_type = self.service.execute(data)
        self.assertEqual(ticket_type.name, 'VIP')
        self.assertEqual(ticket_type.price, Decimal('100.00'))
        self.assertEqual(ticket_type.quantity, 50)
    
    def test_create_with_validation_error(self):
        """Test creating ticket type with invalid data."""
        data = {
            'event_id': self.event_id,
            'name': 'Test',
            'price': Decimal('-10.00'),
            'quantity': 50,
            'sale_start': self.now,
            'sale_end': self.now + timedelta(days=30)
        }
        with self.assertRaises(ValidationError):
            self.service.execute(data)


class UpdateTicketTypeServiceTest(TestCase):
    """Tests for UpdateTicketTypeService."""
    
    def setUp(self):
        self.service = UpdateTicketTypeService()
        self.event_id = uuid.uuid4()
        self.now = timezone.now()
        self.ticket_type = TicketType.objects.create(
            event_id=self.event_id,
            name='General',
            price=Decimal('50.00'),
            quantity=100,
            sale_start=self.now,
            sale_end=self.now + timedelta(days=30)
        )
    
    def test_update_ticket_type(self):
        """Test updating a ticket type."""
        data = {'name': 'General Admission', 'price': Decimal('60.00')}
        updated = self.service.execute(self.ticket_type.id, data)
        self.assertEqual(updated.name, 'General Admission')
        self.assertEqual(updated.price, Decimal('60.00'))
    
    def test_update_nonexistent_ticket_type(self):
        """Test updating non-existent ticket type."""
        with self.assertRaises(ValidationError):
            self.service.execute(uuid.uuid4(), {'name': 'Test'})


class ManageTicketInventoryServiceTest(TestCase):
    """Tests for ManageTicketInventoryService."""
    
    def setUp(self):
        self.service = ManageTicketInventoryService()
        self.event_id = uuid.uuid4()
        self.now = timezone.now()
        self.ticket_type = TicketType.objects.create(
            event_id=self.event_id,
            name='General',
            price=Decimal('50.00'),
            quantity=100,
            sale_start=self.now - timedelta(hours=1),
            sale_end=self.now + timedelta(days=30)
        )
    
    def test_reserve_tickets(self):
        """Test reserving tickets."""
        result = self.service.reserve_tickets(self.ticket_type.id, 10)
        self.assertEqual(result.quantity_sold, 10)
        self.assertEqual(result.available_quantity(), 90)
    
    def test_release_tickets(self):
        """Test releasing tickets."""
        self.ticket_type.quantity_sold = 20
        self.ticket_type.save()
        result = self.service.release_tickets(self.ticket_type.id, 10)
        self.assertEqual(result.quantity_sold, 10)
        self.assertEqual(result.available_quantity(), 90)
    
    def test_get_availability(self):
        """Test getting ticket availability."""
        self.ticket_type.quantity_sold = 30
        self.ticket_type.save()
        availability = self.service.get_availability(self.ticket_type.id)
        self.assertEqual(availability['total_quantity'], 100)
        self.assertEqual(availability['quantity_sold'], 30)
        self.assertEqual(availability['available_quantity'], 70)
        self.assertTrue(availability['is_available'])
    
    def test_reserve_nonexistent_ticket_type(self):
        """Test reserving tickets for non-existent type."""
        with self.assertRaises(ValidationError):
            self.service.reserve_tickets(uuid.uuid4(), 10)
