from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
import uuid

from domain.ticket_type import TicketType


class TicketTypeModelTest(TestCase):
    """Tests for TicketType model."""
    
    def setUp(self):
        self.event_id = uuid.uuid4()
        self.now = timezone.now()
        
    def test_create_ticket_type(self):
        """Test creating a ticket type."""
        ticket_type = TicketType.objects.create(
            event_id=self.event_id,
            name="General Admission",
            price=Decimal('50.00'),
            quantity=100,
            sale_start=self.now,
            sale_end=self.now + timedelta(days=30)
        )
        self.assertEqual(ticket_type.name, "General Admission")
        self.assertEqual(ticket_type.price, Decimal('50.00'))
        self.assertEqual(ticket_type.quantity, 100)
        self.assertEqual(ticket_type.quantity_sold, 0)
    
    def test_negative_price_validation(self):
        """Test that negative price raises validation error."""
        ticket_type = TicketType(
            event_id=self.event_id,
            name="Test",
            price=Decimal('-10.00'),
            quantity=100,
            sale_start=self.now,
            sale_end=self.now + timedelta(days=1)
        )
        with self.assertRaises(ValidationError):
            ticket_type.clean()
    
    def test_negative_quantity_validation(self):
        """Test that negative quantity raises validation error."""
        ticket_type = TicketType(
            event_id=self.event_id,
            name="Test",
            price=Decimal('50.00'),
            quantity=-10,
            sale_start=self.now,
            sale_end=self.now + timedelta(days=1)
        )
        with self.assertRaises(ValidationError):
            ticket_type.clean()
    
    def test_quantity_sold_exceeds_quantity(self):
        """Test that quantity_sold cannot exceed quantity."""
        ticket_type = TicketType(
            event_id=self.event_id,
            name="Test",
            price=Decimal('50.00'),
            quantity=100,
            quantity_sold=150,
            sale_start=self.now,
            sale_end=self.now + timedelta(days=1)
        )
        with self.assertRaises(ValidationError):
            ticket_type.clean()
    
    def test_sale_end_before_start(self):
        """Test that sale_end must be after sale_start."""
        ticket_type = TicketType(
            event_id=self.event_id,
            name="Test",
            price=Decimal('50.00'),
            quantity=100,
            sale_start=self.now,
            sale_end=self.now - timedelta(days=1)
        )
        with self.assertRaises(ValidationError):
            ticket_type.clean()
    
    def test_min_max_purchase_validation(self):
        """Test that max_purchase cannot be less than min_purchase."""
        ticket_type = TicketType(
            event_id=self.event_id,
            name="Test",
            price=Decimal('50.00'),
            quantity=100,
            min_purchase=5,
            max_purchase=2,
            sale_start=self.now,
            sale_end=self.now + timedelta(days=1)
        )
        with self.assertRaises(ValidationError):
            ticket_type.clean()
    
    def test_available_quantity(self):
        """Test available_quantity calculation."""
        ticket_type = TicketType.objects.create(
            event_id=self.event_id,
            name="Test",
            price=Decimal('50.00'),
            quantity=100,
            quantity_sold=30,
            sale_start=self.now,
            sale_end=self.now + timedelta(days=1)
        )
        self.assertEqual(ticket_type.available_quantity(), 70)
    
    def test_is_available(self):
        """Test is_available method."""
        ticket_type = TicketType.objects.create(
            event_id=self.event_id,
            name="Test",
            price=Decimal('50.00'),
            quantity=100,
            sale_start=self.now - timedelta(hours=1),
            sale_end=self.now + timedelta(days=1)
        )
        self.assertTrue(ticket_type.is_available())
    
    def test_is_not_available_sold_out(self):
        """Test is_available returns False when sold out."""
        ticket_type = TicketType.objects.create(
            event_id=self.event_id,
            name="Test",
            price=Decimal('50.00'),
            quantity=100,
            quantity_sold=100,
            sale_start=self.now - timedelta(hours=1),
            sale_end=self.now + timedelta(days=1)
        )
        self.assertFalse(ticket_type.is_available())
    
    def test_is_not_available_inactive(self):
        """Test is_available returns False when inactive."""
        ticket_type = TicketType.objects.create(
            event_id=self.event_id,
            name="Test",
            price=Decimal('50.00'),
            quantity=100,
            is_active=False,
            sale_start=self.now - timedelta(hours=1),
            sale_end=self.now + timedelta(days=1)
        )
        self.assertFalse(ticket_type.is_available())
    
    def test_can_purchase(self):
        """Test can_purchase method."""
        ticket_type = TicketType.objects.create(
            event_id=self.event_id,
            name="Test",
            price=Decimal('50.00'),
            quantity=100,
            min_purchase=1,
            max_purchase=10,
            sale_start=self.now - timedelta(hours=1),
            sale_end=self.now + timedelta(days=1)
        )
        self.assertTrue(ticket_type.can_purchase(5))
        self.assertFalse(ticket_type.can_purchase(15))  # Exceeds max
        self.assertFalse(ticket_type.can_purchase(0))   # Below min
    
    def test_reserve_tickets(self):
        """Test reserve_tickets method."""
        ticket_type = TicketType.objects.create(
            event_id=self.event_id,
            name="Test",
            price=Decimal('50.00'),
            quantity=100,
            sale_start=self.now - timedelta(hours=1),
            sale_end=self.now + timedelta(days=1)
        )
        ticket_type.reserve_tickets(10)
        self.assertEqual(ticket_type.quantity_sold, 10)
        self.assertEqual(ticket_type.available_quantity(), 90)
    
    def test_release_tickets(self):
        """Test release_tickets method."""
        ticket_type = TicketType.objects.create(
            event_id=self.event_id,
            name="Test",
            price=Decimal('50.00'),
            quantity=100,
            quantity_sold=20,
            sale_start=self.now - timedelta(hours=1),
            sale_end=self.now + timedelta(days=1)
        )
        ticket_type.release_tickets(10)
        self.assertEqual(ticket_type.quantity_sold, 10)
        self.assertEqual(ticket_type.available_quantity(), 90)
