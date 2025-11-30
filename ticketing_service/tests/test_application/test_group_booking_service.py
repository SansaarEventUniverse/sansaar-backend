from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError
import uuid

from domain.group_booking import GroupBooking, BulkDiscount
from application.group_booking_service import (
    GroupBookingService,
    BulkDiscountService,
    GroupPaymentService
)


class GroupBookingServiceTest(TestCase):
    """Tests for GroupBookingService."""
    
    def setUp(self):
        self.service = GroupBookingService()
        self.event_id = uuid.uuid4()
        self.organizer_id = uuid.uuid4()
    
    def test_create_booking(self):
        """Test creating group booking."""
        data = {
            'event_id': self.event_id,
            'organizer_id': self.organizer_id,
            'group_name': 'Dev Team',
            'min_participants': 5,
            'max_participants': 10
        }
        
        booking = self.service.create_booking(data)
        
        self.assertEqual(booking.group_name, 'Dev Team')
        self.assertEqual(booking.status, 'pending')
    
    def test_join_booking(self):
        """Test joining group booking."""
        booking = GroupBooking.objects.create(
            event_id=self.event_id,
            organizer_id=self.organizer_id,
            group_name='Test Group',
            min_participants=2,
            max_participants=5
        )
        
        result = self.service.join_booking(booking.id, uuid.uuid4())
        
        self.assertEqual(result['current_participants'], 1)


class BulkDiscountServiceTest(TestCase):
    """Tests for BulkDiscountService."""
    
    def setUp(self):
        self.service = BulkDiscountService()
        self.event_id = uuid.uuid4()
    
    def test_create_discount(self):
        """Test creating bulk discount."""
        data = {
            'event_id': self.event_id,
            'min_quantity': 10,
            'discount_type': 'percentage',
            'discount_value': Decimal('15.00')
        }
        
        discount = self.service.create_discount(data)
        
        self.assertEqual(discount.min_quantity, 10)
        self.assertTrue(discount.is_active)
    
    def test_get_applicable_discount(self):
        """Test getting applicable discount."""
        BulkDiscount.objects.create(
            event_id=self.event_id,
            min_quantity=5,
            discount_type='percentage',
            discount_value=Decimal('10.00')
        )
        
        discount = self.service.get_applicable_discount(self.event_id, 7)
        
        self.assertIsNotNone(discount)
        self.assertEqual(discount.min_quantity, 5)


class GroupPaymentServiceTest(TestCase):
    """Tests for GroupPaymentService."""
    
    def setUp(self):
        self.service = GroupPaymentService()
        self.event_id = uuid.uuid4()
        self.booking = GroupBooking.objects.create(
            event_id=self.event_id,
            organizer_id=uuid.uuid4(),
            group_name='Payment Test',
            min_participants=5,
            max_participants=10,
            current_participants=5
        )
    
    def test_calculate_group_total_no_discount(self):
        """Test calculating total without discount."""
        result = self.service.calculate_group_total(self.booking.id, Decimal('100.00'))
        
        self.assertEqual(result['quantity'], 5)
        self.assertEqual(result['base_total'], '500.00')
        self.assertEqual(result['discount_amount'], '0.00')
    
    def test_calculate_group_total_with_discount(self):
        """Test calculating total with discount."""
        BulkDiscount.objects.create(
            event_id=self.event_id,
            min_quantity=5,
            discount_type='percentage',
            discount_value=Decimal('20.00')
        )
        
        result = self.service.calculate_group_total(self.booking.id, Decimal('100.00'))
        
        self.assertEqual(result['quantity'], 5)
        self.assertEqual(result['final_total'], '400.00')
