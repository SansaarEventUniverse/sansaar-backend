import pytest
from domain.system_health_model import SystemHealth, HealthCheck


@pytest.mark.django_db
class TestSystemHealthModel:
    def test_create_system_health(self):
        health = SystemHealth.objects.create(
            service_name="auth_service",
            status="healthy",
            cpu_usage=45.5,
            memory_usage=60.2
        )
        assert health.service_name == "auth_service"
        assert health.status == "healthy"

    def test_is_critical(self):
        health = SystemHealth.objects.create(
            service_name="payment_service",
            status="critical",
            cpu_usage=95.0,
            memory_usage=90.0
        )
        assert health.is_critical() is True


@pytest.mark.django_db
class TestHealthCheckModel:
    def test_create_health_check(self):
        check = HealthCheck.objects.create(
            service_name="event_service",
            endpoint="/health",
            status="healthy",
            response_time=0.15
        )
        assert check.service_name == "event_service"
        assert check.is_healthy() is True

    def test_unhealthy_check(self):
        check = HealthCheck.objects.create(
            service_name="venue_service",
            endpoint="/health",
            status="unhealthy",
            response_time=5.0
        )
        assert check.is_healthy() is False
