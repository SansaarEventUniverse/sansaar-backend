import pytest
from application.services.analytics_processing_service import AnalyticsProcessingService
from application.services.metric_calculation_service import MetricCalculationService
from application.services.realtime_analytics_service import RealTimeAnalyticsService
from domain.models import AnalyticsEvent


@pytest.mark.django_db
class TestAnalyticsProcessingService:
    def test_process_event(self):
        service = AnalyticsProcessingService()
        event_data = {'event_type': 'page_view', 'event_data': {'page': '/home'}, 'user_id': '123'}
        event = service.process_event(event_data)
        assert event.event_type == 'page_view'
        assert event.is_processed is False

    def test_process_batch_events(self):
        service = AnalyticsProcessingService()
        AnalyticsEvent.objects.create(event_type='view', event_data={})
        AnalyticsEvent.objects.create(event_type='click', event_data={})
        assert service.process_batch_events() == 2


@pytest.mark.django_db
class TestMetricCalculationService:
    def test_calculate_metric(self):
        service = MetricCalculationService()
        AnalyticsEvent.objects.create(event_type='page_view', event_data={})
        AnalyticsEvent.objects.create(event_type='page_view', event_data={})
        metric = service.calculate_metric('total_views', 'page_view', 'count')
        assert metric.metric_value == 2.0

    def test_calculate_aggregated_metrics(self):
        service = MetricCalculationService()
        AnalyticsEvent.objects.create(event_type='page_view', event_data={})
        metrics = service.calculate_aggregated_metrics('hourly')
        assert len(metrics) > 0


@pytest.mark.django_db
class TestRealTimeAnalyticsService:
    def test_get_realtime_metrics(self):
        service = RealTimeAnalyticsService()
        AnalyticsEvent.objects.create(event_type='page_view', event_data={})
        metrics = service.get_realtime_metrics()
        assert 'total_events' in metrics
        assert metrics['total_events'] >= 1

    def test_cache_and_retrieve_data(self):
        service = RealTimeAnalyticsService()
        data = {'views': 100}
        service.cache_realtime_data('test_key', data)
        cached = service.get_cached_data('test_key')
        assert cached['views'] == 100
