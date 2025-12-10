from domain.models import AnalyticsEvent


class AnalyticsProcessingService:
    def process_event(self, event_data):
        return AnalyticsEvent.objects.create(**event_data)

    def process_batch_events(self):
        unprocessed = AnalyticsEvent.get_unprocessed_events()
        count = 0
        for event in unprocessed:
            event.mark_as_processed()
            count += 1
        return count
