import uuid
import json
from typing import Dict, Optional
from domain.analytics import TicketAnalytics


class AnalyticsExportService:
    """Service for exporting analytics data."""
    
    def export_to_csv(self, event_id: uuid.UUID) -> Optional[str]:
        """Export analytics to CSV format."""
        try:
            analytics = TicketAnalytics.objects.get(event_id=event_id)
            
            csv_data = (
                f"event_id,total_tickets,sold_tickets,revenue,sold_percentage\n"
                f"{analytics.event_id},{analytics.total_tickets},"
                f"{analytics.sold_tickets},{analytics.revenue},"
                f"{analytics.calculate_sold_percentage()}"
            )
            
            return csv_data
        except TicketAnalytics.DoesNotExist:
            return None
    
    def export_to_json(self, event_id: uuid.UUID) -> Optional[Dict]:
        """Export analytics to JSON format."""
        try:
            analytics = TicketAnalytics.objects.get(event_id=event_id)
            
            return {
                'event_id': str(analytics.event_id),
                'total_tickets': analytics.total_tickets,
                'sold_tickets': analytics.sold_tickets,
                'revenue': str(analytics.revenue),
                'sold_percentage': analytics.calculate_sold_percentage(),
                'average_price': str(analytics.calculate_average_ticket_price()),
                'is_sold_out': analytics.is_sold_out()
            }
        except TicketAnalytics.DoesNotExist:
            return None
