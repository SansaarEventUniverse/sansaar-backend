from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
import uuid

from domain.ticket_type import TicketType
from domain.order import Order, OrderItem
from infrastructure.repositories.order_repository import (
    OrderRepository,
    InventoryReservationService
)


class OrderRepositoryTest(TestCase):
    """Tests for OrderRepository."""
    
    def setUp(self):
        self.user_id = uuid.uuid4()
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
            user_id=self.user_id,
            event_id=self.event_id,
            total_amount=Decimal('100.00'),
            status='confirmed'
        )
        OrderItem.objects.create(
            order=self.order,
            ticket_type_id=self.ticket_type.id,
            quantity=2,
            unit_price=Decimal('50.00')
        )
        
        self.repository = OrderRepository()
    
    def test_get_user_orders(self):
        """Test getting user orders."""
        orders = self.repository.get_user_orders(self.user_id)
        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0].id, self.order.id)
    
    def test_get_event_orders(self):
        """Test getting event orders."""
        orders = self.repository.get_event_orders(self.event_id)
        self.assertEqual(len(orders), 1)
    
    def test_get_order_analytics(self):
        """Test getting order analytics."""
        analytics = self.repository.get_order_analytics(self.event_id)
        self.assertEqual(analytics['total_revenue'], Decimal('100.00'))
        self.assertEqual(analytics['confirmed_orders'], 1)


class InventoryReservationServiceTest(TestCase):
    """Tests for InventoryReservationService."""
    
    def setUp(self):
        self.service = InventoryReservationService()
    
    def test_create_reservation(self):
        """Test creating a reservation."""
        order_id = uuid.uuid4()
        items = [{'ticket_type_id': uuid.uuid4(), 'quantity': 2}]
        reservation_id = self.service.create_reservation(order_id, items)
        self.assertIsNotNone(reservation_id)
    
    def test_confirm_reservation(self):
        """Test confirming a reservation."""
        order_id = uuid.uuid4()
        items = [{'ticket_type_id': uuid.uuid4(), 'quantity': 2}]
        reservation_id = self.service.create_reservation(order_id, items)
        result = self.service.confirm_reservation(reservation_id)
        self.assertTrue(result)
    
    def test_release_reservation(self):
        """Test releasing a reservation."""
        order_id = uuid.uuid4()
        items = [{'ticket_type_id': uuid.uuid4(), 'quantity': 2}]
        reservation_id = self.service.create_reservation(order_id, items)
        result = self.service.release_reservation(reservation_id)
        self.assertTrue(result)
