from domain.models import PerformanceMetric


class PerformanceMonitoringService:
    def record_metric(self, metric_name: str, metric_value: float, metric_unit: str = "", threshold: float = None):
        return PerformanceMetric.objects.create(
            metric_name=metric_name,
            metric_value=metric_value,
            metric_unit=metric_unit,
            threshold=threshold
        )

    def get_metrics(self):
        return list(PerformanceMetric.objects.all())
