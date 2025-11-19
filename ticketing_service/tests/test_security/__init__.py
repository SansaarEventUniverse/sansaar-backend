from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import timedelta
import uuid

from domain.ticket import Ticket
from domain.ticket_type import TicketType
from domain.order import Order
from application.ticket_service import ValidateQRCodeService, TicketCheckInService


class SecurityTest(TestCase):
    """Security tests for ticketing system."""
    
    def setUp(self):
        self.event_id = uuid.uuid4()
        now = timezone.now()
        
        self.ticket_type = TicketType.objects.create(
            event_id=self.event_id,
            name='Secure Event',
            price=Decimal('100.00'),
            quantity=100,
            sale_start=now - timedelta(days=1),
            sale_end=now + timedelta(days=30)
        )
        
        self.order = Order.objects.create(
            user_id=uuid.uuid4(),
            event_id=self.event_id,
            total_amount=Decimal('100.00'),
            status='confirmed'
        )
        
        self.ticket = Ticket.objects.create(
            ticket_type_id=self.ticket_type.id,
            order_id=self.order.id,
            attendee_name='Test User',
            attendee_email='test@example.com'
        )
    
    def test_qr_code_uniqueness(self):
        """Test that QR codes are unique."""
        ticket2 = Ticket.objects.create(
            ticket_type_id=self.ticket_type.id,
            order_id=self.order.id,
            attendee_name='Test User 2',
            attendee_email='test2@example.com'
        )
        
        self.assertNotEqual(self.ticket.qr_code_data, ticket2.qr_code_data)
    
    def test_invalid_qr_code_validation(self):
        """Test validation fails for invalid QR code."""
        service = ValidateQRCodeService()
        
        with self.assertRaises(ValidationError):
            service.execute('invalid-qr-code')
    
    def test_duplicate_checkin_prevention(self):
        """Test that tickets cannot be checked in twice."""
        service = TicketCheckInService()
        
        # First check-in
        service.execute(self.ticket.id, uuid.uuid4())
        
        # Second check-in should fail
        with self.assertRaises(ValidationError):
            service.execute(self.ticket.id, uuid.uuid4())
    
    def test_negative_price_prevention(self):
        """Test that negative prices are prevented."""
        ticket_type = TicketType(
            event_id=self.event_id,
            name='Invalid',
            price=Decimal('-10.00'),
            quantity=10,
            sale_start=timezone.now(),
            sale_end=timezone.now() + timedelta(days=1)
        )
        
        with self.assertRaises(ValidationError):
            ticket_type.clean()
    
    def test_overselling_prevention(self):
        """Test that overselling is prevented."""
        self.ticket_type.quantity_sold = 100
        self.ticket_type.save()
        
        self.assertFalse(self.ticket_type.can_purchase(1))
