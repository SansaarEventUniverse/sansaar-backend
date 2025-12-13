import json
import csv
from io import StringIO
from domain.models import EventMetrics


class MetricsReportingService:
    def get_event_metrics(self, event_id: str) -> dict:
        metrics = EventMetrics.objects.get(event_id=event_id)
        return {
            'event_id': metrics.event_id,
            'total_views': metrics.total_views,
            'total_registrations': metrics.total_registrations,
            'total_attendance': metrics.total_attendance,
            'revenue': float(metrics.revenue),
            'conversion_rate': metrics.calculate_conversion_rate(),
            'attendance_rate': metrics.calculate_attendance_rate()
        }

    def export_metrics(self, event_id: str, format: str = 'json') -> str:
        metrics = self.get_event_metrics(event_id)
        
        if format == 'csv':
            output = StringIO()
            writer = csv.DictWriter(output, fieldnames=metrics.keys())
            writer.writeheader()
            writer.writerow(metrics)
            return output.getvalue()
        
        return json.dumps(metrics)
