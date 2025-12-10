from infrastructure.repositories.analytics_repository import AnalyticsRepository
from infrastructure.pipeline.event_processor import EventProcessor


class AnalyticsPipeline:
    def __init__(self):
        self.repository = AnalyticsRepository()
        self.processor = EventProcessor()

    def process(self, event_data):
        event = self.repository.save_event(event_data)
        self.processor.process_realtime(event)
        self.processor.index_to_elasticsearch(event)
        event.mark_as_processed()
        return {'status': 'processed', 'event_id': event.id}

    def process_batch(self):
        unprocessed = self.repository.get_unprocessed_events()
        count = 0
        for event in unprocessed:
            self.processor.process_realtime(event)
            self.processor.index_to_elasticsearch(event)
            event.mark_as_processed()
            count += 1
        return count
