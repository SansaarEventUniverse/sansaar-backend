import pytest
from domain.models import PerformanceMetric, SystemHealth
from application.services.performance_monitoring_service import PerformanceMonitoringService
from application.services.system_health_service import SystemHealthService
from application.services.alerting_service import AlertingService


@pytest.mark.django_db
class TestPerformanceMonitoringService:
    def test_record_metric(self):
        service = PerformanceMonitoringService()
        metric = service.record_metric("cpu_usage", 45.0, "percent")
        assert metric.metric_name == "cpu_usage"

    def test_get_metrics(self):
        PerformanceMetric.objects.create(metric_name="cpu", metric_value=50.0)
        service = PerformanceMonitoringService()
        metrics = service.get_metrics()
        assert len(metrics) == 1


@pytest.mark.django_db
class TestSystemHealthService:
    def test_check_health(self):
        service = SystemHealthService()
        health = service.check_health("analytics", 45.0, 60.0)
        assert health.service_name == "analytics"

    def test_get_critical_services(self):
        SystemHealth.objects.create(service_name="s1", status="healthy", cpu_usage=40.0)
        SystemHealth.objects.create(service_name="s2", status="critical", cpu_usage=95.0)
        service = SystemHealthService()
        critical = service.get_critical_services()
        assert len(critical) == 1


@pytest.mark.django_db
class TestAlertingService:
    def test_check_threshold(self):
        metric = PerformanceMetric.objects.create(
            metric_name="cpu",
            metric_value=85.0,
            threshold=80.0
        )
        service = AlertingService()
        alert = service.check_threshold(metric.id)
        assert alert is True

    def test_get_alerts(self):
        PerformanceMetric.objects.create(metric_name="cpu", metric_value=90.0, threshold=80.0)
        service = AlertingService()
        alerts = service.get_alerts()
        assert len(alerts) > 0
