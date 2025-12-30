import pytest
from domain.models import SecurityEvent
from infrastructure.security.threat_detector import ThreatDetector


@pytest.mark.django_db
class TestThreatDetector:
    def test_detect_threat(self):
        SecurityEvent.objects.create(event_type="brute_force", severity="high", source_ip="1.1.1.1", description="Multiple failed logins")
        detector = ThreatDetector()
        threats = detector.detect_threats()
        assert len(threats) > 0
