from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
import uuid
import time

from domain.ticket_type import TicketType
from domain.order import Order, OrderItem
from application.order_service import CreateOrderService, ProcessTicketPurchaseService
from infrastructure.services.qr_code_service import QRCodeService


class PerformanceTest(TestCase):
    """Performance tests for ticket operations."""
    
    def setUp(self):
        self.event_id = uuid.uuid4()
        now = timezone.now()
        
        self.ticket_type = TicketType.objects.create(
            event_id=self.event_id,
            name='Performance Test',
            price=Decimal('50.00'),
            quantity=1000,
            sale_start=now - timedelta(days=1),
            sale_end=now + timedelta(days=30)
        )
    
    def test_bulk_order_creation_performance(self):
        """Test creating multiple orders quickly."""
        start_time = time.time()
        
        service = CreateOrderService()
        orders = []
        for i in range(50):
            order = service.execute({
                'user_id': uuid.uuid4(),
                'event_id': self.event_id,
                'items': [
                    {'ticket_type_id': self.ticket_type.id, 'quantity': 2}
                ]
            })
            orders.append(order)
        
        elapsed = time.time() - start_time
        
        self.assertEqual(len(orders), 50)
        self.assertLess(elapsed, 5.0)  # Should complete in under 5 seconds
    
    def test_ticket_generation_performance(self):
        """Test ticket generation speed."""
        order = Order.objects.create(
            user_id=uuid.uuid4(),
            event_id=self.event_id,
            total_amount=Decimal('500.00')
        )
        OrderItem.objects.create(
            order=order,
            ticket_type_id=self.ticket_type.id,
            quantity=10,
            unit_price=Decimal('50.00')
        )
        
        start_time = time.time()
        
        service = ProcessTicketPurchaseService()
        tickets = service.execute(order.id, uuid.uuid4())
        
        elapsed = time.time() - start_time
        
        self.assertEqual(len(tickets), 10)
        self.assertLess(elapsed, 2.0)  # Should complete in under 2 seconds
    
    def test_qr_code_generation_performance(self):
        """Test QR code generation speed."""
        service = QRCodeService()
        
        start_time = time.time()
        
        qr_codes = []
        for i in range(100):
            qr_code = service.generate_qr_code(str(uuid.uuid4()))
            qr_codes.append(qr_code)
        
        elapsed = time.time() - start_time
        
        self.assertEqual(len(qr_codes), 100)
        self.assertLess(elapsed, 3.0)  # Should complete in under 3 seconds
