import pytest
from django.core.exceptions import ValidationError
from domain.models import PerformanceMetric, SystemHealth


@pytest.mark.django_db
class TestPerformanceMetric:
    def test_create_performance_metric(self):
        metric = PerformanceMetric.objects.create(
            metric_name="response_time",
            metric_value=150.5,
            metric_unit="ms"
        )
        assert metric.metric_name == "response_time"
        assert metric.metric_value == 150.5

    def test_metric_name_required(self):
        with pytest.raises(ValidationError):
            metric = PerformanceMetric(metric_value=100)
            metric.full_clean()

    def test_is_healthy(self):
        metric = PerformanceMetric.objects.create(
            metric_name="cpu_usage",
            metric_value=45.0,
            threshold=80.0
        )
        assert metric.is_healthy() is True


@pytest.mark.django_db
class TestSystemHealth:
    def test_create_system_health(self):
        health = SystemHealth.objects.create(
            service_name="analytics",
            status="healthy",
            cpu_usage=45.0,
            memory_usage=60.0
        )
        assert health.service_name == "analytics"
        assert health.status == "healthy"

    def test_service_name_required(self):
        with pytest.raises(ValidationError):
            health = SystemHealth(status="healthy")
            health.full_clean()

    def test_is_critical(self):
        health = SystemHealth.objects.create(
            service_name="test",
            status="critical",
            cpu_usage=95.0
        )
        assert health.is_critical() is True
