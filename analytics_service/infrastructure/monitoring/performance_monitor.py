from domain.models import PerformanceMetric


class PerformanceMonitor:
    def monitor(self, metric_name: str, metric_value: float):
        metric = PerformanceMetric.objects.create(
            metric_name=metric_name,
            metric_value=metric_value
        )
        return {
            "metric_name": metric.metric_name,
            "metric_value": metric.metric_value
        }
