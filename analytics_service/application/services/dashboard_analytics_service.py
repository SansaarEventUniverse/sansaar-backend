from domain.models import AnalyticsEvent, DashboardWidget


class DashboardAnalyticsService:
    def get_dashboard_data(self, organizer_id):
        total_events = AnalyticsEvent.objects.count()
        unprocessed = AnalyticsEvent.objects.filter(is_processed=False).count()
        return {
            'total_events': total_events,
            'processed_events': total_events - unprocessed,
            'unprocessed_events': unprocessed
        }

    def get_widget_data(self, widget_id):
        widget = DashboardWidget.objects.get(id=widget_id)
        metric = widget.config.get('metric', 'total_events')
        
        if metric == 'total_events':
            return {'value': AnalyticsEvent.objects.count()}
        
        return {'value': 0}
