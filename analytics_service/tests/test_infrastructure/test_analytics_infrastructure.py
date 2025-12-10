import pytest
from infrastructure.pipeline.analytics_pipeline import AnalyticsPipeline
from infrastructure.pipeline.event_processor import EventProcessor
from infrastructure.repositories.analytics_repository import AnalyticsRepository
from domain.models import AnalyticsEvent


@pytest.mark.django_db
class TestAnalyticsPipeline:
    def test_process_event(self):
        pipeline = AnalyticsPipeline()
        event_data = {'event_type': 'page_view', 'event_data': {'page': '/home'}, 'user_id': '123'}
        result = pipeline.process(event_data)
        assert result['status'] == 'processed'

    def test_batch_process(self):
        pipeline = AnalyticsPipeline()
        AnalyticsEvent.objects.create(event_type='view', event_data={})
        AnalyticsEvent.objects.create(event_type='click', event_data={})
        assert pipeline.process_batch() >= 2


@pytest.mark.django_db
class TestEventProcessor:
    def test_process_realtime(self):
        processor = EventProcessor()
        event = AnalyticsEvent.objects.create(event_type='page_view', event_data={'page': '/dashboard'})
        assert processor.process_realtime(event) is True

    def test_index_to_elasticsearch(self):
        processor = EventProcessor()
        event = AnalyticsEvent.objects.create(event_type='click', event_data={'button': 'submit'})
        assert processor.index_to_elasticsearch(event) is True


@pytest.mark.django_db
class TestAnalyticsRepository:
    def test_save_event(self):
        repo = AnalyticsRepository()
        event_data = {'event_type': 'page_view', 'event_data': {'page': '/home'}}
        event = repo.save_event(event_data)
        assert event.id is not None

    def test_get_events_by_type(self):
        repo = AnalyticsRepository()
        AnalyticsEvent.objects.create(event_type='page_view', event_data={})
        AnalyticsEvent.objects.create(event_type='page_view', event_data={})
        AnalyticsEvent.objects.create(event_type='click', event_data={})
        assert repo.get_events_by_type('page_view').count() == 2

    def test_get_events_by_user(self):
        repo = AnalyticsRepository()
        AnalyticsEvent.objects.create(event_type='view', event_data={}, user_id='123')
        AnalyticsEvent.objects.create(event_type='click', event_data={}, user_id='123')
        assert repo.get_events_by_user('123').count() == 2
