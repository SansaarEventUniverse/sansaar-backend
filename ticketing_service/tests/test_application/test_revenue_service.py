from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
import uuid

from domain.revenue import Revenue, RevenueReport
from domain.order import Order
from domain.refund import Refund
from domain.ticket import Ticket
from domain.ticket_type import TicketType
from application.revenue_service import (
    RevenueCalculationService,
    RevenueReportService,
    PayoutManagementService
)


class RevenueCalculationServiceTest(TestCase):
    """Tests for RevenueCalculationService."""
    
    def setUp(self):
        self.service = RevenueCalculationService()
        self.event_id = uuid.uuid4()
        
        self.order = Order.objects.create(
            user_id=uuid.uuid4(),
            event_id=self.event_id,
            total_amount=Decimal('100.00'),
            status='confirmed'
        )
    
    def test_calculate_from_order(self):
        """Test calculating revenue from order."""
        revenue = self.service.calculate_from_order(self.order)
        
        self.assertEqual(revenue.gross_amount, Decimal('100.00'))
        self.assertEqual(revenue.platform_fee, Decimal('10.00'))  # 10%
        self.assertGreater(revenue.payment_fee, Decimal('0.00'))
        self.assertLess(revenue.net_amount, Decimal('100.00'))


class RevenueReportServiceTest(TestCase):
    """Tests for RevenueReportService."""
    
    def setUp(self):
        self.service = RevenueReportService()
        self.event_id = uuid.uuid4()
        
        order = Order.objects.create(
            user_id=uuid.uuid4(),
            event_id=self.event_id,
            total_amount=Decimal('100.00'),
            status='confirmed'
        )
        
        Revenue.objects.create(
            event_id=self.event_id,
            order_id=order.id,
            gross_amount=Decimal('100.00'),
            platform_fee=Decimal('10.00'),
            payment_fee=Decimal('3.00')
        )
    
    def test_generate_daily_report(self):
        """Test generating daily report."""
        report = self.service.generate_report(self.event_id, 'daily')
        
        self.assertEqual(report.period, 'daily')
        self.assertEqual(report.total_gross, Decimal('100.00'))
        self.assertEqual(report.total_orders, 1)


class PayoutManagementServiceTest(TestCase):
    """Tests for PayoutManagementService."""
    
    def setUp(self):
        self.service = PayoutManagementService()
        self.event_id = uuid.uuid4()
        now = timezone.now()
        
        self.ticket_type = TicketType.objects.create(
            event_id=self.event_id,
            name='General',
            price=Decimal('50.00'),
            quantity=100,
            sale_start=now - timedelta(days=1),
            sale_end=now + timedelta(days=30)
        )
        
        order = Order.objects.create(
            user_id=uuid.uuid4(),
            event_id=self.event_id,
            total_amount=Decimal('100.00'),
            status='confirmed'
        )
        
        Revenue.objects.create(
            event_id=self.event_id,
            order_id=order.id,
            gross_amount=Decimal('100.00'),
            platform_fee=Decimal('10.00'),
            payment_fee=Decimal('3.00')
        )
        
        ticket = Ticket.objects.create(
            ticket_type_id=self.ticket_type.id,
            order_id=order.id,
            attendee_name='Test',
            attendee_email='test@example.com'
        )
        
        Refund.objects.create(
            ticket_id=ticket.id,
            order_id=order.id,
            original_amount=Decimal('50.00'),
            refund_amount=Decimal('40.00'),
            reason='Test',
            status='completed'
        )
    
    def test_calculate_payout(self):
        """Test calculating payout."""
        payout = self.service.calculate_payout(self.event_id)
        
        self.assertEqual(payout['total_revenue'], Decimal('87.00'))  # 100 - 10 - 3
        self.assertEqual(payout['total_refunds'], Decimal('40.00'))
        self.assertEqual(payout['payout_amount'], Decimal('47.00'))  # 87 - 40
