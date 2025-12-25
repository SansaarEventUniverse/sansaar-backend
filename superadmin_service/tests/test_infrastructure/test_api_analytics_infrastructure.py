import pytest
from domain.models import APIUsage, APIMetrics
from infrastructure.analytics.usage_tracker import UsageTracker
from infrastructure.analytics.metrics_aggregator import MetricsAggregator


@pytest.mark.django_db
class TestUsageTracker:
    def test_track_api_call(self):
        tracker = UsageTracker()
        usage = tracker.track_api_call("/api/events/", "GET", 200, 0.15)
        assert usage.endpoint == "/api/events/"


@pytest.mark.django_db
class TestMetricsAggregator:
    def test_aggregate_metrics(self):
        APIUsage.objects.create(endpoint="/api/users/", method="GET", status_code=200, response_time=0.1)
        APIUsage.objects.create(endpoint="/api/users/", method="POST", status_code=201, response_time=0.2)
        
        aggregator = MetricsAggregator()
        metrics = aggregator.aggregate_metrics("/api/users/")
        
        assert metrics.endpoint == "/api/users/"
        assert metrics.total_requests == 2
