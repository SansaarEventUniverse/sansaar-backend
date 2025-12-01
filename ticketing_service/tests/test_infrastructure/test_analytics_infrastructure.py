import uuid
from decimal import Decimal
from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from domain.analytics import TicketAnalytics, SalesMetrics
from infrastructure.analytics_pipeline import AnalyticsPipeline
from infrastructure.services.analytics_export import AnalyticsExportService


class AnalyticsPipelineTest(TestCase):
    """Test cases for AnalyticsPipeline."""
    
    def setUp(self):
        self.pipeline = AnalyticsPipeline()
        self.event_id = uuid.uuid4()
    
    def test_process_ticket_sale(self):
        """Test processing ticket sale."""
        result = self.pipeline.process_ticket_sale(
            self.event_id,
            ticket_price=Decimal("100.00")
        )
        
        self.assertTrue(result)
    
    def test_aggregate_sales_data(self):
        """Test aggregating sales data."""
        TicketAnalytics.objects.create(
            event_id=self.event_id,
            total_tickets=100,
            sold_tickets=50,
            revenue=Decimal("5000.00")
        )
        
        data = self.pipeline.aggregate_sales_data(self.event_id)
        
        self.assertIsNotNone(data)
        self.assertEqual(data['sold_tickets'], 50)


class AnalyticsExportServiceTest(TestCase):
    """Test cases for AnalyticsExportService."""
    
    def setUp(self):
        self.service = AnalyticsExportService()
        self.event_id = uuid.uuid4()
    
    def test_export_to_csv(self):
        """Test exporting analytics to CSV."""
        TicketAnalytics.objects.create(
            event_id=self.event_id,
            total_tickets=100,
            sold_tickets=75,
            revenue=Decimal("7500.00")
        )
        
        csv_data = self.service.export_to_csv(self.event_id)
        
        self.assertIsNotNone(csv_data)
        self.assertIn('event_id', csv_data)
    
    def test_export_to_json(self):
        """Test exporting analytics to JSON."""
        TicketAnalytics.objects.create(
            event_id=self.event_id,
            total_tickets=100,
            sold_tickets=75,
            revenue=Decimal("7500.00")
        )
        
        json_data = self.service.export_to_json(self.event_id)
        
        self.assertIsNotNone(json_data)
        self.assertIn('event_id', json_data)
