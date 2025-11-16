from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
import uuid

from domain.ticket import Ticket


class TicketModelTest(TestCase):
    """Tests for Ticket model."""
    
    def setUp(self):
        self.ticket_type_id = uuid.uuid4()
        self.order_id = uuid.uuid4()
    
    def test_create_ticket(self):
        """Test creating a ticket."""
        ticket = Ticket.objects.create(
            ticket_type_id=self.ticket_type_id,
            order_id=self.order_id,
            attendee_name="John Doe",
            attendee_email="john@example.com"
        )
        self.assertEqual(ticket.attendee_name, "John Doe")
        self.assertEqual(ticket.status, 'active')
        self.assertIsNotNone(ticket.qr_code_data)
        self.assertIsNotNone(ticket.security_hash)
    
    def test_generate_qr_data(self):
        """Test QR code data generation."""
        ticket = Ticket.objects.create(
            ticket_type_id=self.ticket_type_id,
            order_id=self.order_id,
            attendee_name="John Doe",
            attendee_email="john@example.com"
        )
        expected = f"{ticket.id}|{self.ticket_type_id}|{self.order_id}"
        self.assertEqual(ticket.qr_code_data, expected)
    
    def test_generate_security_hash(self):
        """Test security hash generation."""
        ticket = Ticket.objects.create(
            ticket_type_id=self.ticket_type_id,
            order_id=self.order_id,
            attendee_name="John Doe",
            attendee_email="john@example.com"
        )
        self.assertEqual(len(ticket.security_hash), 64)  # SHA256 hash length
    
    def test_validate_security_hash(self):
        """Test security hash validation."""
        ticket = Ticket.objects.create(
            ticket_type_id=self.ticket_type_id,
            order_id=self.order_id,
            attendee_name="John Doe",
            attendee_email="john@example.com"
        )
        self.assertTrue(ticket.validate_security_hash(ticket.security_hash))
        self.assertFalse(ticket.validate_security_hash("invalid_hash"))
    
    def test_can_check_in(self):
        """Test can_check_in method."""
        ticket = Ticket.objects.create(
            ticket_type_id=self.ticket_type_id,
            order_id=self.order_id,
            attendee_name="John Doe",
            attendee_email="john@example.com"
        )
        self.assertTrue(ticket.can_check_in())
    
    def test_cannot_check_in_used_ticket(self):
        """Test cannot check in used ticket."""
        ticket = Ticket.objects.create(
            ticket_type_id=self.ticket_type_id,
            order_id=self.order_id,
            attendee_name="John Doe",
            attendee_email="john@example.com",
            status='used'
        )
        self.assertFalse(ticket.can_check_in())
    
    def test_check_in(self):
        """Test ticket check-in."""
        ticket = Ticket.objects.create(
            ticket_type_id=self.ticket_type_id,
            order_id=self.order_id,
            attendee_name="John Doe",
            attendee_email="john@example.com"
        )
        staff_id = uuid.uuid4()
        ticket.check_in(staff_id)
        
        self.assertEqual(ticket.status, 'used')
        self.assertIsNotNone(ticket.checked_in_at)
        self.assertEqual(ticket.checked_in_by, staff_id)
    
    def test_check_in_already_used(self):
        """Test checking in already used ticket raises error."""
        ticket = Ticket.objects.create(
            ticket_type_id=self.ticket_type_id,
            order_id=self.order_id,
            attendee_name="John Doe",
            attendee_email="john@example.com",
            status='used',
            checked_in_at=timezone.now()
        )
        with self.assertRaises(ValidationError):
            ticket.check_in(uuid.uuid4())
    
    def test_cancel_ticket(self):
        """Test cancelling a ticket."""
        ticket = Ticket.objects.create(
            ticket_type_id=self.ticket_type_id,
            order_id=self.order_id,
            attendee_name="John Doe",
            attendee_email="john@example.com"
        )
        ticket.cancel()
        self.assertEqual(ticket.status, 'cancelled')
    
    def test_cannot_cancel_used_ticket(self):
        """Test cannot cancel used ticket."""
        ticket = Ticket.objects.create(
            ticket_type_id=self.ticket_type_id,
            order_id=self.order_id,
            attendee_name="John Doe",
            attendee_email="john@example.com",
            status='used'
        )
        with self.assertRaises(ValidationError):
            ticket.cancel()
    
    def test_is_valid(self):
        """Test is_valid method."""
        ticket = Ticket.objects.create(
            ticket_type_id=self.ticket_type_id,
            order_id=self.order_id,
            attendee_name="John Doe",
            attendee_email="john@example.com"
        )
        self.assertTrue(ticket.is_valid())
        
        ticket.status = 'used'
        ticket.save()
        self.assertFalse(ticket.is_valid())
