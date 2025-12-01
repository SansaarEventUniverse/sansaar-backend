import uuid
from decimal import Decimal
from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from domain.analytics import TicketAnalytics, SalesMetrics


class TicketAnalyticsTest(TestCase):
    """Test cases for TicketAnalytics model."""
    
    def setUp(self):
        self.event_id = uuid.uuid4()
    
    def test_create_ticket_analytics(self):
        """Test creating ticket analytics."""
        analytics = TicketAnalytics.objects.create(
            event_id=self.event_id,
            total_tickets=100,
            sold_tickets=75,
            revenue=Decimal("7500.00")
        )
        
        self.assertIsNotNone(analytics.id)
        self.assertEqual(analytics.event_id, self.event_id)
        self.assertEqual(analytics.total_tickets, 100)
        self.assertEqual(analytics.sold_tickets, 75)
    
    def test_calculate_sold_percentage(self):
        """Test calculating sold percentage."""
        analytics = TicketAnalytics.objects.create(
            event_id=self.event_id,
            total_tickets=100,
            sold_tickets=75,
            revenue=Decimal("7500.00")
        )
        
        percentage = analytics.calculate_sold_percentage()
        self.assertEqual(percentage, 75.0)
    
    def test_calculate_average_ticket_price(self):
        """Test calculating average ticket price."""
        analytics = TicketAnalytics.objects.create(
            event_id=self.event_id,
            total_tickets=100,
            sold_tickets=50,
            revenue=Decimal("5000.00")
        )
        
        avg_price = analytics.calculate_average_ticket_price()
        self.assertEqual(avg_price, Decimal("100.00"))
    
    def test_is_sold_out(self):
        """Test checking if event is sold out."""
        analytics = TicketAnalytics.objects.create(
            event_id=self.event_id,
            total_tickets=100,
            sold_tickets=100,
            revenue=Decimal("10000.00")
        )
        
        self.assertTrue(analytics.is_sold_out())


class SalesMetricsTest(TestCase):
    """Test cases for SalesMetrics model."""
    
    def setUp(self):
        self.event_id = uuid.uuid4()
    
    def test_create_sales_metrics(self):
        """Test creating sales metrics."""
        metrics = SalesMetrics.objects.create(
            event_id=self.event_id,
            period_start=timezone.now() - timedelta(days=7),
            period_end=timezone.now(),
            total_sales=Decimal("10000.00"),
            transaction_count=100
        )
        
        self.assertIsNotNone(metrics.id)
        self.assertEqual(metrics.event_id, self.event_id)
        self.assertEqual(metrics.total_sales, Decimal("10000.00"))
    
    def test_calculate_average_transaction_value(self):
        """Test calculating average transaction value."""
        metrics = SalesMetrics.objects.create(
            event_id=self.event_id,
            period_start=timezone.now() - timedelta(days=7),
            period_end=timezone.now(),
            total_sales=Decimal("10000.00"),
            transaction_count=100
        )
        
        avg_value = metrics.calculate_average_transaction_value()
        self.assertEqual(avg_value, Decimal("100.00"))
    
    def test_calculate_daily_average(self):
        """Test calculating daily average sales."""
        start = timezone.now() - timedelta(days=7)
        end = timezone.now()
        
        metrics = SalesMetrics.objects.create(
            event_id=self.event_id,
            period_start=start,
            period_end=end,
            total_sales=Decimal("7000.00"),
            transaction_count=70
        )
        
        daily_avg = metrics.calculate_daily_average()
        self.assertEqual(daily_avg, Decimal("1000.00"))
    
    def test_get_growth_rate(self):
        """Test calculating growth rate."""
        metrics = SalesMetrics.objects.create(
            event_id=self.event_id,
            period_start=timezone.now() - timedelta(days=7),
            period_end=timezone.now(),
            total_sales=Decimal("12000.00"),
            transaction_count=120,
            previous_period_sales=Decimal("10000.00")
        )
        
        growth_rate = metrics.get_growth_rate()
        self.assertEqual(growth_rate, 20.0)
