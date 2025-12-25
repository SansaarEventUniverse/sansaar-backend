import pytest
from domain.api_analytics_model import APIUsage, APIMetrics


@pytest.mark.django_db
class TestAPIUsageModel:
    def test_create_api_usage(self):
        usage = APIUsage.objects.create(
            endpoint="/api/events/",
            method="GET",
            status_code=200,
            response_time=0.15
        )
        assert usage.endpoint == "/api/events/"
        assert usage.method == "GET"

    def test_is_successful(self):
        usage = APIUsage.objects.create(
            endpoint="/api/users/",
            method="POST",
            status_code=201,
            response_time=0.25
        )
        assert usage.is_successful() is True

    def test_is_not_successful(self):
        usage = APIUsage.objects.create(
            endpoint="/api/events/",
            method="GET",
            status_code=500,
            response_time=1.5
        )
        assert usage.is_successful() is False


@pytest.mark.django_db
class TestAPIMetricsModel:
    def test_create_api_metrics(self):
        metrics = APIMetrics.objects.create(
            endpoint="/api/events/",
            total_requests=1000,
            successful_requests=950,
            failed_requests=50
        )
        assert metrics.endpoint == "/api/events/"
        assert metrics.total_requests == 1000

    def test_success_rate(self):
        metrics = APIMetrics.objects.create(
            endpoint="/api/users/",
            total_requests=100,
            successful_requests=95,
            failed_requests=5
        )
        assert metrics.success_rate() == 95.0
