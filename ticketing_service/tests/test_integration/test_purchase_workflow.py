from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
import uuid

from domain.ticket_type import TicketType
from domain.order import Order, OrderItem
from domain.ticket import Ticket
from application.order_service import CreateOrderService, ProcessTicketPurchaseService
from application.ticket_type_service import CreateTicketTypeService


class PurchaseWorkflowIntegrationTest(TestCase):
    """Integration tests for complete purchase workflow."""
    
    def setUp(self):
        self.event_id = uuid.uuid4()
        self.user_id = uuid.uuid4()
        now = timezone.now()
        
        # Create ticket type
        service = CreateTicketTypeService()
        self.ticket_type = service.execute({
            'event_id': self.event_id,
            'name': 'VIP Pass',
            'description': 'VIP access',
            'price': Decimal('100.00'),
            'quantity': 50,
            'sale_start': now - timedelta(days=1),
            'sale_end': now + timedelta(days=30)
        })
    
    def test_complete_purchase_workflow(self):
        """Test complete purchase from order to ticket generation."""
        # Step 1: Create order
        create_service = CreateOrderService()
        order = create_service.execute({
            'user_id': self.user_id,
            'event_id': self.event_id,
            'items': [
                {'ticket_type_id': self.ticket_type.id, 'quantity': 3}
            ]
        })
        
        self.assertEqual(order.status, 'pending')
        self.assertEqual(order.total_amount, Decimal('300.00'))
        self.assertEqual(order.items.count(), 1)
        
        # Step 2: Process purchase
        purchase_service = ProcessTicketPurchaseService()
        payment_id = uuid.uuid4()
        tickets = purchase_service.execute(order.id, payment_id)
        
        self.assertEqual(len(tickets), 3)
        
        # Step 3: Verify order confirmed
        order.refresh_from_db()
        self.assertEqual(order.status, 'confirmed')
        self.assertEqual(order.payment_id, payment_id)
        
        # Step 4: Verify inventory updated
        self.ticket_type.refresh_from_db()
        self.assertEqual(self.ticket_type.quantity_sold, 3)
        self.assertEqual(self.ticket_type.available_quantity(), 47)
        
        # Step 5: Verify tickets generated
        for ticket in tickets:
            self.assertEqual(ticket.ticket_type_id, self.ticket_type.id)
            self.assertEqual(ticket.order_id, order.id)
            self.assertIsNotNone(ticket.qr_code_data)
    
    def test_multiple_ticket_types_purchase(self):
        """Test purchasing multiple ticket types in one order."""
        now = timezone.now()
        
        # Create second ticket type
        service = CreateTicketTypeService()
        ticket_type2 = service.execute({
            'event_id': self.event_id,
            'name': 'General',
            'price': Decimal('50.00'),
            'quantity': 100,
            'sale_start': now - timedelta(days=1),
            'sale_end': now + timedelta(days=30)
        })
        
        # Create order with multiple types
        create_service = CreateOrderService()
        order = create_service.execute({
            'user_id': self.user_id,
            'event_id': self.event_id,
            'items': [
                {'ticket_type_id': self.ticket_type.id, 'quantity': 2},
                {'ticket_type_id': ticket_type2.id, 'quantity': 3}
            ]
        })
        
        self.assertEqual(order.total_amount, Decimal('350.00'))  # 2*100 + 3*50
        self.assertEqual(order.items.count(), 2)
        
        # Process purchase
        purchase_service = ProcessTicketPurchaseService()
        tickets = purchase_service.execute(order.id, uuid.uuid4())
        
        self.assertEqual(len(tickets), 5)


class InventoryManagementIntegrationTest(TestCase):
    """Integration tests for inventory management."""
    
    def setUp(self):
        self.event_id = uuid.uuid4()
        now = timezone.now()
        
        self.ticket_type = TicketType.objects.create(
            event_id=self.event_id,
            name='Limited Edition',
            price=Decimal('200.00'),
            quantity=10,
            sale_start=now - timedelta(days=1),
            sale_end=now + timedelta(days=30)
        )
    
    def test_concurrent_purchase_inventory_tracking(self):
        """Test inventory tracking with concurrent purchases."""
        # Create multiple orders
        orders = []
        for i in range(3):
            order = Order.objects.create(
                user_id=uuid.uuid4(),
                event_id=self.event_id,
                total_amount=Decimal('200.00')
            )
            OrderItem.objects.create(
                order=order,
                ticket_type_id=self.ticket_type.id,
                quantity=2,
                unit_price=Decimal('200.00')
            )
            orders.append(order)
        
        # Process all purchases
        service = ProcessTicketPurchaseService()
        for order in orders:
            service.execute(order.id, uuid.uuid4())
        
        # Verify total inventory
        self.ticket_type.refresh_from_db()
        self.assertEqual(self.ticket_type.quantity_sold, 6)
        self.assertEqual(self.ticket_type.available_quantity(), 4)
    
    def test_sold_out_prevention(self):
        """Test that sold out tickets cannot be purchased."""
        # Sell all tickets
        self.ticket_type.quantity_sold = 10
        self.ticket_type.save()
        
        # Try to create order
        from django.core.exceptions import ValidationError
        service = CreateOrderService()
        
        with self.assertRaises(ValidationError):
            service.execute({
                'user_id': uuid.uuid4(),
                'event_id': self.event_id,
                'items': [
                    {'ticket_type_id': self.ticket_type.id, 'quantity': 1}
                ]
            })
