from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError
import uuid

from domain.group_booking import GroupBooking, BulkDiscount


class GroupBookingModelTest(TestCase):
    """Tests for GroupBooking model."""
    
    def setUp(self):
        self.event_id = uuid.uuid4()
        self.organizer_id = uuid.uuid4()
    
    def test_create_group_booking(self):
        """Test creating a group booking."""
        booking = GroupBooking.objects.create(
            event_id=self.event_id,
            organizer_id=self.organizer_id,
            group_name='Tech Team',
            min_participants=5,
            max_participants=10
        )
        
        self.assertEqual(booking.status, 'pending')
        self.assertEqual(booking.current_participants, 0)
    
    def test_add_participant(self):
        """Test adding participant to group."""
        booking = GroupBooking.objects.create(
            event_id=self.event_id,
            organizer_id=self.organizer_id,
            group_name='Marketing Team',
            min_participants=3,
            max_participants=5,
            status='active'
        )
        
        booking.add_participant()
        self.assertEqual(booking.current_participants, 1)
    
    def test_group_becomes_active(self):
        """Test group becomes active when min reached."""
        booking = GroupBooking.objects.create(
            event_id=self.event_id,
            organizer_id=self.organizer_id,
            group_name='Sales Team',
            min_participants=2,
            max_participants=5,
            status='pending'
        )
        
        booking.add_participant()
        booking.add_participant()
        
        self.assertTrue(booking.is_complete())
        self.assertEqual(booking.status, 'active')
    
    def test_cannot_exceed_max_participants(self):
        """Test cannot exceed max participants."""
        booking = GroupBooking.objects.create(
            event_id=self.event_id,
            organizer_id=self.organizer_id,
            group_name='Small Team',
            min_participants=1,
            max_participants=2,
            current_participants=2,
            status='active'
        )
        
        with self.assertRaises(ValidationError):
            booking.add_participant()


class BulkDiscountModelTest(TestCase):
    """Tests for BulkDiscount model."""
    
    def setUp(self):
        self.event_id = uuid.uuid4()
    
    def test_create_bulk_discount(self):
        """Test creating bulk discount."""
        discount = BulkDiscount.objects.create(
            event_id=self.event_id,
            min_quantity=10,
            discount_type='percentage',
            discount_value=Decimal('15.00')
        )
        
        self.assertTrue(discount.is_active)
    
    def test_percentage_discount(self):
        """Test percentage discount calculation."""
        discount = BulkDiscount.objects.create(
            event_id=self.event_id,
            min_quantity=5,
            discount_type='percentage',
            discount_value=Decimal('10.00')
        )
        
        result = discount.calculate_discount(5, Decimal('100.00'))
        self.assertEqual(result, Decimal('10.00'))
    
    def test_fixed_discount(self):
        """Test fixed discount calculation."""
        discount = BulkDiscount.objects.create(
            event_id=self.event_id,
            min_quantity=10,
            discount_type='fixed',
            discount_value=Decimal('5.00')
        )
        
        result = discount.calculate_discount(10, Decimal('50.00'))
        self.assertEqual(result, Decimal('5.00'))
    
    def test_apply_discount(self):
        """Test applying discount to total."""
        discount = BulkDiscount.objects.create(
            event_id=self.event_id,
            min_quantity=5,
            discount_type='percentage',
            discount_value=Decimal('20.00')
        )
        
        total = Decimal('500.00')
        result = discount.apply_discount(5, total)
        self.assertEqual(result, Decimal('400.00'))
    
    def test_no_discount_below_min(self):
        """Test no discount below minimum quantity."""
        discount = BulkDiscount.objects.create(
            event_id=self.event_id,
            min_quantity=10,
            discount_type='percentage',
            discount_value=Decimal('15.00')
        )
        
        total = Decimal('500.00')
        result = discount.apply_discount(5, total)
        self.assertEqual(result, total)
