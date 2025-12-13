from django.db import transaction
from domain.models import EventMetrics


class EventAnalyticsService:
    @transaction.atomic
    def track_event_view(self, event_id: str) -> EventMetrics:
        metrics, _ = EventMetrics.objects.get_or_create(event_id=event_id)
        metrics.total_views += 1
        metrics.save()
        return metrics

    @transaction.atomic
    def track_event_registration(self, event_id: str) -> EventMetrics:
        metrics, _ = EventMetrics.objects.get_or_create(event_id=event_id)
        metrics.total_registrations += 1
        metrics.save()
        return metrics

    @transaction.atomic
    def update_revenue(self, event_id: str, amount) -> EventMetrics:
        metrics, _ = EventMetrics.objects.get_or_create(event_id=event_id)
        metrics.revenue += amount
        metrics.save()
        return metrics
