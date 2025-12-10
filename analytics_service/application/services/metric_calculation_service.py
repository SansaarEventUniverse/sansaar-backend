from domain.models import AnalyticsEvent, MetricCalculation
from django.utils import timezone
from datetime import timedelta


class MetricCalculationService:
    def calculate_metric(self, metric_name, event_type, calculation_type):
        value = AnalyticsEvent.objects.filter(event_type=event_type).count()
        return MetricCalculation.objects.create(
            metric_name=metric_name,
            metric_value=float(value),
            calculation_type=calculation_type
        )

    def calculate_aggregated_metrics(self, time_period):
        now = timezone.now()
        start_time = now - timedelta(hours=1 if time_period == 'hourly' else 24)
        events = AnalyticsEvent.objects.filter(created_at__gte=start_time)
        total = events.count()
        metric = MetricCalculation.objects.create(
            metric_name='total_events',
            metric_value=float(total),
            calculation_type='count',
            time_period=time_period
        )
        return [metric]
