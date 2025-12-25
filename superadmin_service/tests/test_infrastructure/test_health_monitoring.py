import pytest
from domain.models import SystemHealth, HealthCheck
from infrastructure.monitoring.health_monitor import HealthMonitor
from infrastructure.monitoring.alert_system import AlertSystem


@pytest.mark.django_db
class TestHealthMonitor:
    def test_monitor_service(self):
        monitor = HealthMonitor()
        health = monitor.monitor_service("auth_service")
        assert health is not None

    def test_check_service_endpoint(self):
        monitor = HealthMonitor()
        check = monitor.check_service_endpoint("event_service", "/health")
        assert check is not None


@pytest.mark.django_db
class TestAlertSystem:
    def test_check_critical_services(self):
        SystemHealth.objects.create(service_name="payment_service", status="critical", cpu_usage=95.0, memory_usage=90.0)
        alert_system = AlertSystem()
        alerts = alert_system.check_critical_services()
        assert len(alerts) > 0
