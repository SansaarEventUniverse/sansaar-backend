import pytest
from rest_framework.test import APIClient
from domain.models import APIUsage, APIMetrics


@pytest.mark.django_db
class TestAPIAnalyticsAPI:
    def test_get_api_analytics(self):
        APIUsage.objects.create(endpoint="/api/events/", method="GET", status_code=200, response_time=0.1)
        client = APIClient()
        response = client.get('/api/superadmin/admin/api-analytics/')
        assert response.status_code == 200

    def test_api_usage_report(self):
        APIUsage.objects.create(endpoint="/api/users/", method="POST", status_code=201, response_time=0.2)
        client = APIClient()
        response = client.get('/api/superadmin/admin/api-usage/')
        assert response.status_code == 200
        assert len(response.data) == 1

    def test_api_monitoring(self):
        APIMetrics.objects.create(endpoint="/api/events/", total_requests=100, successful_requests=95, failed_requests=5)
        client = APIClient()
        response = client.get('/api/superadmin/admin/api-monitoring/')
        assert response.status_code == 200
        assert len(response.data) == 1
