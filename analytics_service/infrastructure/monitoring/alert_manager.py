from domain.models import PerformanceMetric


class AlertManager:
    def trigger_alert(self, metric_id: int):
        metric = PerformanceMetric.objects.get(id=metric_id)
        return not metric.is_healthy()
