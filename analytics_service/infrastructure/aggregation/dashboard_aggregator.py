from domain.models import AnalyticsEvent


class DashboardAggregator:
    def aggregate_dashboard_data(self, organizer_id):
        total_events = AnalyticsEvent.objects.count()
        unprocessed = AnalyticsEvent.objects.filter(is_processed=False).count()
        
        return {
            'total_events': total_events,
            'processed_events': total_events - unprocessed,
            'unprocessed_events': unprocessed
        }
