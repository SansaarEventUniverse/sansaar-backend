import pytest
from rest_framework.test import APIClient
from domain.models import SystemHealth, HealthCheck


@pytest.mark.django_db
class TestSystemHealthAPI:
    def test_get_system_health(self):
        SystemHealth.objects.create(service_name="auth_service", status="healthy", cpu_usage=45.0, memory_usage=50.0)
        client = APIClient()
        response = client.get('/api/superadmin/admin/system-health/')
        assert response.status_code == 200
        assert len(response.data) == 1

    def test_health_check(self):
        HealthCheck.objects.create(service_name="event_service", endpoint="/health", status="healthy", response_time=0.1)
        client = APIClient()
        response = client.get('/api/superadmin/admin/health-check/')
        assert response.status_code == 200
        assert len(response.data) == 1

    def test_monitoring_dashboard(self):
        SystemHealth.objects.create(service_name="payment_service", status="warning", cpu_usage=80.0, memory_usage=75.0)
        client = APIClient()
        response = client.get('/api/superadmin/admin/monitoring/')
        assert response.status_code == 200
