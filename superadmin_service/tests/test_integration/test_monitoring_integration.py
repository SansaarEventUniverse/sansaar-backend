import pytest
from domain.models import SystemHealth, HealthCheck, APIUsage, APIMetrics, Notification, SecurityEvent
from application.services.system_health_service import SystemHealthService
from application.services.api_analytics_service import APIAnalyticsService
from application.services.notification_service import NotificationService
from application.services.security_monitoring_service import SecurityMonitoringService
from infrastructure.monitoring.health_monitor import HealthMonitor
from infrastructure.analytics.metrics_aggregator import MetricsAggregator
from infrastructure.notifications.notification_dispatcher import NotificationDispatcher
from infrastructure.security.threat_detector import ThreatDetector


@pytest.mark.django_db
class TestHealthMonitoringIntegration:
    def test_health_monitoring_workflow(self):
        monitor = HealthMonitor()
        health = monitor.monitor_service("test_service")
        
        assert health.service_name == "test_service"
        assert health.status in ["healthy", "warning", "critical"]


@pytest.mark.django_db
class TestAPIAnalyticsIntegration:
    def test_usage_tracking_workflow(self):
        APIUsage.objects.create(endpoint="/api/test/", method="GET", status_code=200, response_time=0.1)
        APIUsage.objects.create(endpoint="/api/test/", method="POST", status_code=201, response_time=0.2)
        
        aggregator = MetricsAggregator()
        metrics = aggregator.aggregate_metrics("/api/test/")
        
        assert metrics.total_requests == 2
        assert metrics.successful_requests == 2


@pytest.mark.django_db
class TestNotificationIntegration:
    def test_notification_delivery_workflow(self):
        service = NotificationService()
        notification = service.create_notification("Alert", "Test message", "alert")
        
        dispatcher = NotificationDispatcher()
        result = dispatcher.dispatch(notification.id)
        
        assert result["status"] == "dispatched"


@pytest.mark.django_db
class TestSecurityMonitoringIntegration:
    def test_threat_detection_workflow(self):
        service = SecurityMonitoringService()
        event = service.log_event("attack", "critical", "1.1.1.1", "DDoS attack detected")
        
        detector = ThreatDetector()
        threats = detector.detect_threats()
        
        assert len(threats) > 0
        assert event in threats
