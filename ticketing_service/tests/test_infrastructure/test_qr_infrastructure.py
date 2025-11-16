from django.test import TestCase
import uuid

from domain.ticket import Ticket
from infrastructure.services.qr_code_service import QRCodeService
from infrastructure.repositories.ticket_repository import TicketRepository


class QRCodeServiceTest(TestCase):
    """Tests for QRCodeService."""
    
    def setUp(self):
        self.service = QRCodeService()
    
    def test_generate_qr_code(self):
        """Test QR code generation."""
        data = "test_qr_data"
        qr_code = self.service.generate_qr_code(data)
        self.assertTrue(qr_code.startswith("data:image/png;base64,"))
    
    def test_generate_qr_image(self):
        """Test QR code image generation."""
        data = "test_qr_data"
        img_bytes = self.service.generate_qr_image(data)
        self.assertIsInstance(img_bytes, bytes)
        self.assertGreater(len(img_bytes), 0)


class TicketRepositoryTest(TestCase):
    """Tests for TicketRepository."""
    
    def setUp(self):
        self.repository = TicketRepository()
        self.order_id = uuid.uuid4()
        self.ticket_type_id = uuid.uuid4()
        
        # Create test tickets
        Ticket.objects.create(
            ticket_type_id=self.ticket_type_id,
            order_id=self.order_id,
            attendee_name='John Doe',
            attendee_email='john@example.com',
            status='active'
        )
        Ticket.objects.create(
            ticket_type_id=self.ticket_type_id,
            order_id=self.order_id,
            attendee_name='Jane Doe',
            attendee_email='jane@example.com',
            status='used'
        )
    
    def test_get_by_order(self):
        """Test getting tickets by order."""
        tickets = self.repository.get_by_order(self.order_id)
        self.assertEqual(len(tickets), 2)
    
    def test_get_active_tickets(self):
        """Test getting active tickets."""
        tickets = self.repository.get_active_tickets(self.order_id)
        self.assertEqual(len(tickets), 1)
        self.assertEqual(tickets[0].status, 'active')
    
    def test_get_checked_in_count(self):
        """Test getting checked-in count."""
        count = self.repository.get_checked_in_count(self.ticket_type_id)
        self.assertEqual(count, 1)
