import pytest
from rest_framework.test import APIClient
from domain.models import PerformanceMetric, SystemHealth


@pytest.mark.django_db
class TestPerformanceAPI:
    def test_get_performance(self):
        PerformanceMetric.objects.create(metric_name="cpu", metric_value=45.0)
        client = APIClient()
        response = client.get('/api/analytics/admin/performance/')
        assert response.status_code == 200
        assert len(response.data) == 1


@pytest.mark.django_db
class TestSystemHealthAPI:
    def test_get_system_health(self):
        SystemHealth.objects.create(service_name="analytics", status="healthy", cpu_usage=45.0)
        client = APIClient()
        response = client.get('/api/analytics/admin/system-health/')
        assert response.status_code == 200
        assert len(response.data) == 1


@pytest.mark.django_db
class TestAlertsAPI:
    def test_get_alerts(self):
        PerformanceMetric.objects.create(metric_name="cpu", metric_value=90.0, threshold=80.0)
        client = APIClient()
        response = client.get('/api/analytics/admin/alerts/')
        assert response.status_code == 200
        assert len(response.data) > 0
