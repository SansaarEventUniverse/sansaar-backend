import pytest
from domain.models import APIUsage, APIMetrics
from application.services.api_analytics_service import APIAnalyticsService
from application.services.usage_tracking_service import UsageTrackingService
from application.services.api_monitoring_service import APIMonitoringService


@pytest.mark.django_db
class TestAPIAnalyticsService:
    def test_get_endpoint_analytics(self):
        APIUsage.objects.create(endpoint="/api/events/", method="GET", status_code=200, response_time=0.1)
        service = APIAnalyticsService()
        analytics = service.get_endpoint_analytics("/api/events/")
        assert analytics is not None


@pytest.mark.django_db
class TestUsageTrackingService:
    def test_track_request(self):
        service = UsageTrackingService()
        usage = service.track_request("/api/users/", "POST", 201, 0.25)
        assert usage.endpoint == "/api/users/"

    def test_get_usage_stats(self):
        APIUsage.objects.create(endpoint="/api/events/", method="GET", status_code=200, response_time=0.1)
        service = UsageTrackingService()
        stats = service.get_usage_stats("/api/events/")
        assert stats["total_requests"] == 1


@pytest.mark.django_db
class TestAPIMonitoringService:
    def test_get_all_metrics(self):
        APIMetrics.objects.create(endpoint="/api/events/", total_requests=100, successful_requests=95, failed_requests=5)
        service = APIMonitoringService()
        metrics = service.get_all_metrics()
        assert len(metrics) == 1
