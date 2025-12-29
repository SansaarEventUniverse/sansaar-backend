import pytest
from domain.security_model import SecurityEvent, SecurityRule


@pytest.mark.django_db
class TestSecurityEventModel:
    def test_create_security_event(self):
        event = SecurityEvent.objects.create(
            event_type="unauthorized_access",
            severity="high",
            source_ip="192.168.1.100",
            description="Failed login attempt"
        )
        assert event.event_type == "unauthorized_access"
        assert event.is_critical() is True

    def test_is_not_critical(self):
        event = SecurityEvent.objects.create(
            event_type="info",
            severity="low",
            source_ip="192.168.1.1",
            description="Normal activity"
        )
        assert event.is_critical() is False


@pytest.mark.django_db
class TestSecurityRuleModel:
    def test_create_security_rule(self):
        rule = SecurityRule.objects.create(
            name="Brute Force Detection",
            rule_type="login_attempts",
            threshold=5,
            is_active=True
        )
        assert rule.name == "Brute Force Detection"
        assert rule.is_active is True
