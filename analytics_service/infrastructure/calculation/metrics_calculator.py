from domain.models import EventMetrics


class MetricsCalculator:
    def calculate_conversion_rate(self, event_id: str) -> float:
        metrics = EventMetrics.objects.get(event_id=event_id)
        return metrics.calculate_conversion_rate()

    def calculate_attendance_rate(self, event_id: str) -> float:
        metrics = EventMetrics.objects.get(event_id=event_id)
        return metrics.calculate_attendance_rate()
