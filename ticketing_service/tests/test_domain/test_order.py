from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError
import uuid

from domain.order import Order, OrderItem


class OrderModelTest(TestCase):
    """Tests for Order model."""
    
    def setUp(self):
        self.user_id = uuid.uuid4()
        self.event_id = uuid.uuid4()
    
    def test_create_order(self):
        """Test creating an order."""
        order = Order.objects.create(
            user_id=self.user_id,
            event_id=self.event_id,
            total_amount=Decimal('100.00')
        )
        self.assertEqual(order.status, 'pending')
        self.assertEqual(order.total_amount, Decimal('100.00'))
    
    def test_negative_amount_validation(self):
        """Test negative amount validation."""
        order = Order(
            user_id=self.user_id,
            event_id=self.event_id,
            total_amount=Decimal('-10.00')
        )
        with self.assertRaises(ValidationError):
            order.clean()
    
    def test_confirm_order(self):
        """Test confirming an order."""
        order = Order.objects.create(
            user_id=self.user_id,
            event_id=self.event_id,
            total_amount=Decimal('100.00')
        )
        payment_id = uuid.uuid4()
        order.confirm(payment_id)
        self.assertEqual(order.status, 'confirmed')
        self.assertEqual(order.payment_id, payment_id)
    
    def test_cannot_confirm_non_pending(self):
        """Test cannot confirm non-pending order."""
        order = Order.objects.create(
            user_id=self.user_id,
            event_id=self.event_id,
            total_amount=Decimal('100.00'),
            status='confirmed'
        )
        with self.assertRaises(ValidationError):
            order.confirm(uuid.uuid4())
    
    def test_cancel_order(self):
        """Test cancelling an order."""
        order = Order.objects.create(
            user_id=self.user_id,
            event_id=self.event_id,
            total_amount=Decimal('100.00')
        )
        order.cancel()
        self.assertEqual(order.status, 'cancelled')
    
    def test_cannot_cancel_confirmed(self):
        """Test cannot cancel confirmed order."""
        order = Order.objects.create(
            user_id=self.user_id,
            event_id=self.event_id,
            total_amount=Decimal('100.00'),
            status='confirmed'
        )
        with self.assertRaises(ValidationError):
            order.cancel()


class OrderItemModelTest(TestCase):
    """Tests for OrderItem model."""
    
    def setUp(self):
        self.order = Order.objects.create(
            user_id=uuid.uuid4(),
            event_id=uuid.uuid4(),
            total_amount=Decimal('0.00')
        )
    
    def test_create_order_item(self):
        """Test creating an order item."""
        item = OrderItem.objects.create(
            order=self.order,
            ticket_type_id=uuid.uuid4(),
            quantity=2,
            unit_price=Decimal('50.00')
        )
        self.assertEqual(item.quantity, 2)
        self.assertEqual(item.subtotal, Decimal('100.00'))
    
    def test_subtotal_calculation(self):
        """Test subtotal is calculated automatically."""
        item = OrderItem.objects.create(
            order=self.order,
            ticket_type_id=uuid.uuid4(),
            quantity=3,
            unit_price=Decimal('25.00')
        )
        self.assertEqual(item.subtotal, Decimal('75.00'))
    
    def test_negative_quantity_validation(self):
        """Test negative quantity validation."""
        item = OrderItem(
            order=self.order,
            ticket_type_id=uuid.uuid4(),
            quantity=-1,
            unit_price=Decimal('50.00')
        )
        with self.assertRaises(ValidationError):
            item.clean()
