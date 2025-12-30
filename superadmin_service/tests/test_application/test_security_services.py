import pytest
from domain.models import SecurityEvent
from application.services.security_monitoring_service import SecurityMonitoringService


@pytest.mark.django_db
class TestSecurityMonitoringService:
    def test_log_security_event(self):
        service = SecurityMonitoringService()
        event = service.log_event("unauthorized_access", "high", "192.168.1.1", "Test")
        assert event.event_type == "unauthorized_access"

    def test_get_critical_events(self):
        SecurityEvent.objects.create(event_type="attack", severity="critical", source_ip="1.1.1.1", description="Test")
        service = SecurityMonitoringService()
        events = service.get_critical_events()
        assert len(events) == 1
