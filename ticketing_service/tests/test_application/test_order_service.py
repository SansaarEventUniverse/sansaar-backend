from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
import uuid

from domain.ticket_type import TicketType
from domain.order import Order, OrderItem
from application.order_service import (
    CreateOrderService,
    ProcessTicketPurchaseService,
    OrderManagementService
)


class CreateOrderServiceTest(TestCase):
    """Tests for CreateOrderService."""
    
    def setUp(self):
        self.event_id = uuid.uuid4()
        now = timezone.now()
        self.ticket_type = TicketType.objects.create(
            event_id=self.event_id,
            name="General Admission",
            price=Decimal('50.00'),
            quantity=100,
            sale_start=now - timedelta(days=1),
            sale_end=now + timedelta(days=30)
        )
        self.service = CreateOrderService()
    
    def test_create_order_with_items(self):
        """Test creating order with items."""
        data = {
            'user_id': uuid.uuid4(),
            'event_id': self.event_id,
            'items': [
                {'ticket_type_id': self.ticket_type.id, 'quantity': 2}
            ]
        }
        order = self.service.execute(data)
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.total_amount, Decimal('100.00'))
    
    def test_create_order_insufficient_tickets(self):
        """Test creating order with insufficient tickets."""
        data = {
            'user_id': uuid.uuid4(),
            'event_id': self.event_id,
            'items': [
                {'ticket_type_id': self.ticket_type.id, 'quantity': 200}
            ]
        }
        with self.assertRaises(ValidationError):
            self.service.execute(data)


class ProcessTicketPurchaseServiceTest(TestCase):
    """Tests for ProcessTicketPurchaseService."""
    
    def setUp(self):
        self.event_id = uuid.uuid4()
        now = timezone.now()
        self.ticket_type = TicketType.objects.create(
            event_id=self.event_id,
            name="General Admission",
            price=Decimal('50.00'),
            quantity=100,
            sale_start=now - timedelta(days=1),
            sale_end=now + timedelta(days=30)
        )
        self.order = Order.objects.create(
            user_id=uuid.uuid4(),
            event_id=self.event_id,
            total_amount=Decimal('100.00')
        )
        OrderItem.objects.create(
            order=self.order,
            ticket_type_id=self.ticket_type.id,
            quantity=2,
            unit_price=Decimal('50.00')
        )
        self.service = ProcessTicketPurchaseService()
    
    def test_process_purchase(self):
        """Test processing purchase."""
        payment_id = uuid.uuid4()
        tickets = self.service.execute(self.order.id, payment_id)
        self.assertEqual(len(tickets), 2)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'confirmed')
    
    def test_process_invalid_order(self):
        """Test processing invalid order."""
        with self.assertRaises(ValidationError):
            self.service.execute(uuid.uuid4(), uuid.uuid4())


class OrderManagementServiceTest(TestCase):
    """Tests for OrderManagementService."""
    
    def setUp(self):
        self.event_id = uuid.uuid4()
        now = timezone.now()
        self.ticket_type = TicketType.objects.create(
            event_id=self.event_id,
            name="General Admission",
            price=Decimal('50.00'),
            quantity=100,
            sale_start=now - timedelta(days=1),
            sale_end=now + timedelta(days=30)
        )
        self.order = Order.objects.create(
            user_id=uuid.uuid4(),
            event_id=self.event_id,
            total_amount=Decimal('100.00')
        )
        OrderItem.objects.create(
            order=self.order,
            ticket_type_id=self.ticket_type.id,
            quantity=2,
            unit_price=Decimal('50.00')
        )
        self.service = OrderManagementService()
    
    def test_get_order(self):
        """Test getting order."""
        order = self.service.get_order(self.order.id)
        self.assertEqual(order.id, self.order.id)
    
    def test_cancel_order(self):
        """Test cancelling order."""
        order = self.service.cancel_order(self.order.id)
        self.assertEqual(order.status, 'cancelled')
