import pytest
from django.core.exceptions import ValidationError
from domain.models import AnalyticsEvent, MetricCalculation


@pytest.mark.django_db
class TestAnalyticsEvent:
    def test_create_analytics_event(self):
        event = AnalyticsEvent.objects.create(
            event_type='page_view',
            event_data={'page': '/dashboard'},
            user_id='123'
        )
        assert event.event_type == 'page_view'
        assert event.is_processed is False

    def test_event_type_validation(self):
        event = AnalyticsEvent(event_type='', event_data={})
        with pytest.raises(ValidationError):
            event.full_clean()

    def test_mark_as_processed(self):
        event = AnalyticsEvent.objects.create(event_type='click', event_data={})
        event.mark_as_processed()
        assert event.is_processed is True
        assert event.processed_at is not None

    def test_get_unprocessed_events(self):
        AnalyticsEvent.objects.create(event_type='view', event_data={})
        AnalyticsEvent.objects.create(event_type='click', event_data={}, is_processed=True)
        assert AnalyticsEvent.get_unprocessed_events().count() == 1


@pytest.mark.django_db
class TestMetricCalculation:
    def test_create_metric(self):
        metric = MetricCalculation.objects.create(
            metric_name='total_views',
            metric_value=100.0,
            calculation_type='sum'
        )
        assert metric.metric_name == 'total_views'
        assert metric.metric_value == 100.0

    def test_metric_name_validation(self):
        metric = MetricCalculation(metric_name='', metric_value=50.0, calculation_type='avg')
        with pytest.raises(ValidationError):
            metric.full_clean()

    def test_calculate_percentage_change(self):
        metric = MetricCalculation.objects.create(
            metric_name='views',
            metric_value=150.0,
            previous_value=100.0,
            calculation_type='sum'
        )
        assert metric.calculate_percentage_change() == 50.0

    def test_get_latest_metrics(self):
        MetricCalculation.objects.create(metric_name='views', metric_value=100, calculation_type='sum')
        MetricCalculation.objects.create(metric_name='clicks', metric_value=50, calculation_type='sum')
        assert MetricCalculation.get_latest_metrics().count() == 2
