from domain.models import PerformanceMetric


class AlertingService:
    def check_threshold(self, metric_id: int):
        metric = PerformanceMetric.objects.get(id=metric_id)
        return not metric.is_healthy()

    def get_alerts(self):
        metrics = PerformanceMetric.objects.exclude(threshold__isnull=True)
        return [m for m in metrics if not m.is_healthy()]
