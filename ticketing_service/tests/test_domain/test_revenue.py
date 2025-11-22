from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
import uuid

from domain.revenue import Revenue, RevenueReport


class RevenueModelTest(TestCase):
    """Tests for Revenue model."""
    
    def setUp(self):
        self.event_id = uuid.uuid4()
        self.order_id = uuid.uuid4()
    
    def test_create_revenue(self):
        """Test creating revenue."""
        revenue = Revenue.objects.create(
            event_id=self.event_id,
            order_id=self.order_id,
            gross_amount=Decimal('100.00'),
            platform_fee=Decimal('10.00'),
            payment_fee=Decimal('3.00')
        )
        
        self.assertEqual(revenue.net_amount, Decimal('87.00'))
    
    def test_calculate_net(self):
        """Test net amount calculation."""
        revenue = Revenue(
            event_id=self.event_id,
            order_id=self.order_id,
            gross_amount=Decimal('200.00'),
            platform_fee=Decimal('20.00'),
            payment_fee=Decimal('5.00')
        )
        
        net = revenue.calculate_net()
        self.assertEqual(net, Decimal('175.00'))
    
    def test_negative_amount_validation(self):
        """Test negative amount validation."""
        revenue = Revenue(
            event_id=self.event_id,
            order_id=self.order_id,
            gross_amount=Decimal('-100.00')
        )
        
        with self.assertRaises(ValidationError):
            revenue.clean()


class RevenueReportModelTest(TestCase):
    """Tests for RevenueReport model."""
    
    def setUp(self):
        self.event_id = uuid.uuid4()
        self.now = timezone.now()
    
    def test_create_report(self):
        """Test creating a revenue report."""
        report = RevenueReport.objects.create(
            event_id=self.event_id,
            period='daily',
            start_date=self.now,
            end_date=self.now + timedelta(days=1),
            total_gross=Decimal('1000.00'),
            total_fees=Decimal('100.00'),
            total_net=Decimal('900.00'),
            total_orders=10
        )
        
        self.assertEqual(report.total_net, Decimal('900.00'))
        self.assertEqual(report.total_orders, 10)
    
    def test_invalid_date_range(self):
        """Test invalid date range validation."""
        report = RevenueReport(
            event_id=self.event_id,
            period='daily',
            start_date=self.now,
            end_date=self.now - timedelta(days=1)
        )
        
        with self.assertRaises(ValidationError):
            report.clean()
