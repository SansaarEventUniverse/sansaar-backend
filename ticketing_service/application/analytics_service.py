import uuid
from decimal import Decimal
from typing import Dict, Optional
from django.utils import timezone
from domain.analytics import TicketAnalytics, SalesMetrics


class TicketAnalyticsService:
    """Service for managing ticket analytics."""
    
    def get_or_create_analytics(self, event_id: uuid.UUID) -> TicketAnalytics:
        """Get or create analytics for an event."""
        analytics, created = TicketAnalytics.objects.get_or_create(
            event_id=event_id,
            defaults={
                'total_tickets': 0,
                'sold_tickets': 0,
                'revenue': Decimal("0.00")
            }
        )
        return analytics
    
    def update_ticket_sales(
        self,
        event_id: uuid.UUID,
        total_tickets: int,
        sold_tickets: int,
        revenue: Decimal
    ) -> TicketAnalytics:
        """Update ticket sales analytics."""
        analytics = self.get_or_create_analytics(event_id)
        analytics.total_tickets = total_tickets
        analytics.sold_tickets = sold_tickets
        analytics.revenue = revenue
        analytics.save()
        return analytics
    
    def get_event_analytics(self, event_id: uuid.UUID) -> Optional[Dict]:
        """Get event analytics with calculations."""
        try:
            analytics = TicketAnalytics.objects.get(event_id=event_id)
            return {
                'event_id': str(analytics.event_id),
                'total_tickets': analytics.total_tickets,
                'sold_tickets': analytics.sold_tickets,
                'revenue': analytics.revenue,
                'sold_percentage': analytics.calculate_sold_percentage(),
                'average_price': analytics.calculate_average_ticket_price(),
                'is_sold_out': analytics.is_sold_out()
            }
        except TicketAnalytics.DoesNotExist:
            return None


class SalesReportingService:
    """Service for sales reporting."""
    
    def create_sales_report(
        self,
        event_id: uuid.UUID,
        period_start,
        period_end,
        total_sales: Decimal,
        transaction_count: int,
        previous_period_sales: Decimal = Decimal("0.00")
    ) -> SalesMetrics:
        """Create a sales report."""
        metrics = SalesMetrics.objects.create(
            event_id=event_id,
            period_start=period_start,
            period_end=period_end,
            total_sales=total_sales,
            transaction_count=transaction_count,
            previous_period_sales=previous_period_sales
        )
        return metrics
    
    def get_period_report(
        self,
        event_id: uuid.UUID,
        period_start,
        period_end
    ) -> Optional[Dict]:
        """Get sales report for a period."""
        try:
            metrics = SalesMetrics.objects.filter(
                event_id=event_id,
                period_start=period_start,
                period_end=period_end
            ).first()
            
            if not metrics:
                return None
            
            return {
                'event_id': str(metrics.event_id),
                'period_start': metrics.period_start,
                'period_end': metrics.period_end,
                'total_sales': metrics.total_sales,
                'transaction_count': metrics.transaction_count,
                'average_transaction_value': metrics.calculate_average_transaction_value(),
                'daily_average': metrics.calculate_daily_average(),
                'growth_rate': metrics.get_growth_rate()
            }
        except Exception:
            return None


class BusinessIntelligenceService:
    """Service for business intelligence."""
    
    def __init__(self):
        self.analytics_service = TicketAnalyticsService()
        self.reporting_service = SalesReportingService()
    
    def get_comprehensive_metrics(self, event_id: uuid.UUID) -> Dict:
        """Get comprehensive metrics for an event."""
        ticket_analytics = self.analytics_service.get_event_analytics(event_id)
        
        sales_metrics = SalesMetrics.objects.filter(event_id=event_id).order_by('-created_at').first()
        sales_data = None
        if sales_metrics:
            sales_data = {
                'total_sales': sales_metrics.total_sales,
                'transaction_count': sales_metrics.transaction_count,
                'average_transaction_value': sales_metrics.calculate_average_transaction_value()
            }
        
        return {
            'ticket_analytics': ticket_analytics,
            'sales_metrics': sales_data
        }
    
    def calculate_kpis(self, event_id: uuid.UUID) -> Dict:
        """Calculate key performance indicators."""
        analytics = TicketAnalytics.objects.filter(event_id=event_id).first()
        
        if not analytics:
            return {}
        
        return {
            'conversion_rate': analytics.calculate_sold_percentage(),
            'revenue_per_ticket': analytics.calculate_average_ticket_price(),
            'total_revenue': analytics.revenue,
            'tickets_remaining': analytics.total_tickets - analytics.sold_tickets
        }
