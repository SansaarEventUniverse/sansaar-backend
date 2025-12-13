from domain.models import EventMetrics


class EventAnalyticsRepository:
    def save_metrics(self, event_id: str, **kwargs) -> EventMetrics:
        metrics, _ = EventMetrics.objects.update_or_create(
            event_id=event_id,
            defaults=kwargs
        )
        return metrics

    def get_metrics(self, event_id: str) -> EventMetrics:
        return EventMetrics.objects.get(event_id=event_id)
