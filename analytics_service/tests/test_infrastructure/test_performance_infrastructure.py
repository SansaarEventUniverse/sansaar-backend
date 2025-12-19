import pytest
from domain.models import PerformanceMetric, SystemHealth
from infrastructure.monitoring.performance_monitor import PerformanceMonitor
from infrastructure.monitoring.health_tracker import HealthTracker
from infrastructure.monitoring.alert_manager import AlertManager


@pytest.mark.django_db
class TestPerformanceMonitor:
    def test_monitor_metric(self):
        monitor = PerformanceMonitor()
        result = monitor.monitor("cpu_usage", 45.0)
        assert "metric_name" in result


@pytest.mark.django_db
class TestHealthTracker:
    def test_track_health(self):
        tracker = HealthTracker()
        result = tracker.track("analytics", 45.0, 60.0)
        assert result.service_name == "analytics"


@pytest.mark.django_db
class TestAlertManager:
    def test_trigger_alert(self):
        metric = PerformanceMetric.objects.create(
            metric_name="cpu",
            metric_value=90.0,
            threshold=80.0
        )
        manager = AlertManager()
        alert = manager.trigger_alert(metric.id)
        assert alert is True
