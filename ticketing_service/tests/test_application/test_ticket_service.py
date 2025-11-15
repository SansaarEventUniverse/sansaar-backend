from django.test import TestCase
from django.core.exceptions import ValidationError
import uuid

from domain.ticket import Ticket
from application.ticket_service import (
    GenerateTicketService,
    ValidateQRCodeService,
    TicketCheckInService
)


class GenerateTicketServiceTest(TestCase):
    """Tests for GenerateTicketService."""
    
    def setUp(self):
        self.service = GenerateTicketService()
        self.ticket_type_id = uuid.uuid4()
        self.order_id = uuid.uuid4()
    
    def test_generate_ticket(self):
        """Test generating a ticket."""
        data = {
            'ticket_type_id': self.ticket_type_id,
            'order_id': self.order_id,
            'attendee_name': 'John Doe',
            'attendee_email': 'john@example.com'
        }
        ticket = self.service.execute(data)
        self.assertEqual(ticket.attendee_name, 'John Doe')
        self.assertIsNotNone(ticket.qr_code_data)
    
    def test_bulk_generate(self):
        """Test bulk ticket generation."""
        data = {
            'ticket_type_id': self.ticket_type_id,
            'order_id': self.order_id,
            'attendee_name': 'John Doe',
            'attendee_email': 'john@example.com'
        }
        tickets = self.service.bulk_generate(data, 5)
        self.assertEqual(len(tickets), 5)


class ValidateQRCodeServiceTest(TestCase):
    """Tests for ValidateQRCodeService."""
    
    def setUp(self):
        self.service = ValidateQRCodeService()
        self.ticket = Ticket.objects.create(
            ticket_type_id=uuid.uuid4(),
            order_id=uuid.uuid4(),
            attendee_name='John Doe',
            attendee_email='john@example.com'
        )
    
    def test_validate_qr_code(self):
        """Test validating QR code."""
        result = self.service.execute(self.ticket.qr_code_data)
        self.assertTrue(result['valid'])
        self.assertEqual(result['ticket_id'], str(self.ticket.id))
        self.assertEqual(result['status'], 'active')
    
    def test_validate_invalid_qr_code(self):
        """Test validating invalid QR code."""
        with self.assertRaises(ValidationError):
            self.service.execute('invalid_qr_code')


class TicketCheckInServiceTest(TestCase):
    """Tests for TicketCheckInService."""
    
    def setUp(self):
        self.service = TicketCheckInService()
        self.ticket = Ticket.objects.create(
            ticket_type_id=uuid.uuid4(),
            order_id=uuid.uuid4(),
            attendee_name='John Doe',
            attendee_email='john@example.com'
        )
    
    def test_check_in_ticket(self):
        """Test checking in a ticket."""
        staff_id = uuid.uuid4()
        result = self.service.execute(self.ticket.id, staff_id)
        self.assertEqual(result.status, 'used')
        self.assertIsNotNone(result.checked_in_at)
    
    def test_check_in_by_qr(self):
        """Test checking in by QR code."""
        staff_id = uuid.uuid4()
        result = self.service.check_in_by_qr(self.ticket.qr_code_data, staff_id)
        self.assertEqual(result.status, 'used')
    
    def test_check_in_nonexistent_ticket(self):
        """Test checking in non-existent ticket."""
        with self.assertRaises(ValidationError):
            self.service.execute(uuid.uuid4(), uuid.uuid4())
