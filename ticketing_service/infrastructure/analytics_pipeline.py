import uuid
from decimal import Decimal
from typing import Dict, Optional
from domain.analytics import TicketAnalytics
from application.analytics_service import TicketAnalyticsService


class AnalyticsPipeline:
    """Pipeline for processing analytics data."""
    
    def __init__(self):
        self.analytics_service = TicketAnalyticsService()
    
    def process_ticket_sale(
        self,
        event_id: uuid.UUID,
        ticket_price: Decimal
    ) -> bool:
        """Process a ticket sale and update analytics."""
        try:
            analytics = self.analytics_service.get_or_create_analytics(event_id)
            analytics.sold_tickets += 1
            analytics.revenue += ticket_price
            analytics.save()
            return True
        except Exception:
            return False
    
    def aggregate_sales_data(self, event_id: uuid.UUID) -> Optional[Dict]:
        """Aggregate sales data for an event."""
        try:
            analytics = TicketAnalytics.objects.get(event_id=event_id)
            return {
                'event_id': str(analytics.event_id),
                'total_tickets': analytics.total_tickets,
                'sold_tickets': analytics.sold_tickets,
                'revenue': analytics.revenue,
                'sold_percentage': analytics.calculate_sold_percentage()
            }
        except TicketAnalytics.DoesNotExist:
            return None
