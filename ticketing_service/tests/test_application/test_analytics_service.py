import uuid
from decimal import Decimal
from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from domain.analytics import TicketAnalytics, SalesMetrics
from application.analytics_service import (
    TicketAnalyticsService,
    SalesReportingService,
    BusinessIntelligenceService
)


class TicketAnalyticsServiceTest(TestCase):
    """Test cases for TicketAnalyticsService."""
    
    def setUp(self):
        self.service = TicketAnalyticsService()
        self.event_id = uuid.uuid4()
    
    def test_get_or_create_analytics(self):
        """Test getting or creating analytics."""
        analytics = self.service.get_or_create_analytics(self.event_id)
        
        self.assertIsNotNone(analytics.id)
        self.assertEqual(analytics.event_id, self.event_id)
    
    def test_update_ticket_sales(self):
        """Test updating ticket sales."""
        analytics = self.service.update_ticket_sales(
            self.event_id,
            total_tickets=100,
            sold_tickets=50,
            revenue=Decimal("5000.00")
        )
        
        self.assertEqual(analytics.total_tickets, 100)
        self.assertEqual(analytics.sold_tickets, 50)
        self.assertEqual(analytics.revenue, Decimal("5000.00"))
    
    def test_get_event_analytics(self):
        """Test getting event analytics."""
        TicketAnalytics.objects.create(
            event_id=self.event_id,
            total_tickets=100,
            sold_tickets=75,
            revenue=Decimal("7500.00")
        )
        
        analytics = self.service.get_event_analytics(self.event_id)
        
        self.assertIsNotNone(analytics)
        self.assertEqual(analytics['sold_percentage'], 75.0)


class SalesReportingServiceTest(TestCase):
    """Test cases for SalesReportingService."""
    
    def setUp(self):
        self.service = SalesReportingService()
        self.event_id = uuid.uuid4()
    
    def test_create_sales_report(self):
        """Test creating sales report."""
        start = timezone.now() - timedelta(days=7)
        end = timezone.now()
        
        report = self.service.create_sales_report(
            self.event_id,
            start,
            end,
            total_sales=Decimal("10000.00"),
            transaction_count=100
        )
        
        self.assertIsNotNone(report.id)
        self.assertEqual(report.total_sales, Decimal("10000.00"))
    
    def test_get_period_report(self):
        """Test getting period report."""
        start = timezone.now() - timedelta(days=7)
        end = timezone.now()
        
        SalesMetrics.objects.create(
            event_id=self.event_id,
            period_start=start,
            period_end=end,
            total_sales=Decimal("10000.00"),
            transaction_count=100
        )
        
        report = self.service.get_period_report(self.event_id, start, end)
        
        self.assertIsNotNone(report)
        self.assertEqual(report['total_sales'], Decimal("10000.00"))


class BusinessIntelligenceServiceTest(TestCase):
    """Test cases for BusinessIntelligenceService."""
    
    def setUp(self):
        self.service = BusinessIntelligenceService()
        self.event_id = uuid.uuid4()
    
    def test_get_comprehensive_metrics(self):
        """Test getting comprehensive metrics."""
        TicketAnalytics.objects.create(
            event_id=self.event_id,
            total_tickets=100,
            sold_tickets=75,
            revenue=Decimal("7500.00")
        )
        
        metrics = self.service.get_comprehensive_metrics(self.event_id)
        
        self.assertIn('ticket_analytics', metrics)
        self.assertIn('sales_metrics', metrics)
    
    def test_calculate_kpis(self):
        """Test calculating KPIs."""
        TicketAnalytics.objects.create(
            event_id=self.event_id,
            total_tickets=100,
            sold_tickets=75,
            revenue=Decimal("7500.00")
        )
        
        kpis = self.service.calculate_kpis(self.event_id)
        
        self.assertIn('conversion_rate', kpis)
        self.assertIn('revenue_per_ticket', kpis)
