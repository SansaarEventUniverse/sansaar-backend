import uuid
from decimal import Decimal
from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from domain.analytics import TicketAnalytics, SalesMetrics


class AnalyticsAPITest(TestCase):
    """Test cases for Analytics API endpoints."""
    
    def setUp(self):
        self.client = APIClient()
        self.event_id = uuid.uuid4()
    
    def test_get_ticket_analytics(self):
        """Test getting ticket analytics."""
        TicketAnalytics.objects.create(
            event_id=self.event_id,
            total_tickets=100,
            sold_tickets=75,
            revenue=Decimal("7500.00")
        )
        
        response = self.client.get(f'/api/tickets/events/{self.event_id}/ticket-analytics/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['sold_percentage'], 75.0)
    
    def test_get_sales_report(self):
        """Test getting sales report."""
        start = timezone.now() - timedelta(days=7)
        end = timezone.now()
        
        SalesMetrics.objects.create(
            event_id=self.event_id,
            period_start=start,
            period_end=end,
            total_sales=Decimal("10000.00"),
            transaction_count=100
        )
        
        response = self.client.get(
            f'/api/tickets/events/{self.event_id}/sales-report/',
            {'start': start.isoformat(), 'end': end.isoformat()}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_sales', response.data)
    
    def test_get_business_intelligence(self):
        """Test getting business intelligence."""
        TicketAnalytics.objects.create(
            event_id=self.event_id,
            total_tickets=100,
            sold_tickets=75,
            revenue=Decimal("7500.00")
        )
        
        response = self.client.get(f'/api/tickets/events/{self.event_id}/business-intelligence/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('ticket_analytics', response.data)
        self.assertIn('sales_metrics', response.data)
