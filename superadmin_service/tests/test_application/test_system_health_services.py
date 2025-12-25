import pytest
from domain.models import SystemHealth, HealthCheck
from application.services.system_health_service import SystemHealthService
from application.services.health_check_service import HealthCheckService
from application.services.monitoring_service import MonitoringService


@pytest.mark.django_db
class TestSystemHealthService:
    def test_record_health(self):
        service = SystemHealthService()
        health = service.record_health("auth_service", "healthy", 45.0, 60.0)
        assert health.service_name == "auth_service"

    def test_get_service_health(self):
        SystemHealth.objects.create(service_name="event_service", status="healthy", cpu_usage=50.0, memory_usage=55.0)
        service = SystemHealthService()
        health = service.get_service_health("event_service")
        assert health is not None


@pytest.mark.django_db
class TestHealthCheckService:
    def test_perform_check(self):
        service = HealthCheckService()
        check = service.perform_check("payment_service", "/health", "healthy", 0.2)
        assert check.service_name == "payment_service"

    def test_get_recent_checks(self):
        HealthCheck.objects.create(service_name="venue_service", endpoint="/health", status="healthy", response_time=0.1)
        service = HealthCheckService()
        checks = service.get_recent_checks("venue_service")
        assert len(checks) == 1


@pytest.mark.django_db
class TestMonitoringService:
    def test_get_all_services_health(self):
        SystemHealth.objects.create(service_name="auth_service", status="healthy", cpu_usage=40.0, memory_usage=50.0)
        SystemHealth.objects.create(service_name="event_service", status="warning", cpu_usage=75.0, memory_usage=70.0)
        service = MonitoringService()
        health_data = service.get_all_services_health()
        assert len(health_data) == 2
