from datetime import timedelta
from unittest.mock import MagicMock, patch

import pytest
from django.utils import timezone

from application.security_monitoring_application_service import SecurityMonitoringApplicationService
from domain.audit_log_model import AuditEventType
from domain.models import AuditLog


@pytest.mark.django_db
class TestSecurityMonitoringApplicationService:
    def setup_method(self):
        self.service = SecurityMonitoringApplicationService()

    @patch("infrastructure.services.security_monitoring_service.AlertService.send_alert")
    def test_detect_suspicious_activity_with_alerts(self, mock_send_alert):
        time_now = timezone.now()
        for i in range(6):
            log = AuditLog.objects.create(
                event_type=AuditEventType.LOGIN, user_id="1", success=False
            )
            AuditLog.objects.filter(id=log.id).update(created_at=time_now - timedelta(minutes=i))

        result = self.service.detect_suspicious_activity("1")

        assert result["user_id"] == "1"
        assert result["suspicious"] is True
        assert "FAILED_LOGIN_SPIKE" in result["alerts"]

    @patch("infrastructure.services.security_monitoring_service.AlertService.send_alert")
    def test_detect_suspicious_activity_no_alerts(self, mock_send_alert):
        result = self.service.detect_suspicious_activity("1")

        assert result["user_id"] == "1"
        assert result["suspicious"] is False
        assert len(result["alerts"]) == 0

    @patch("infrastructure.services.security_monitoring_service.AlertService.send_alert")
    def test_monitor_system_security_with_alerts(self, mock_send_alert):
        time_now = timezone.now()
        for i in range(11):
            log = AuditLog.objects.create(
                event_type=AuditEventType.ACCOUNT_LOCKED, user_id=str(i), success=True
            )
            AuditLog.objects.filter(id=log.id).update(created_at=time_now - timedelta(minutes=i))

        result = self.service.monitor_system_security()

        assert result["alert_count"] > 0
        assert "ACCOUNT_LOCKOUT_SPIKE" in result["alerts"]

    @patch("infrastructure.services.security_monitoring_service.AlertService.send_alert")
    def test_monitor_system_security_no_alerts(self, mock_send_alert):
        result = self.service.monitor_system_security()

        assert result["alert_count"] == 0
        assert len(result["alerts"]) == 0

    @patch("infrastructure.services.alert_service.AlertService.send_alert")
    def test_generate_alert(self, mock_send_alert):
        mock_send_alert.return_value = {"email_sent": True, "slack_sent": True}

        result = self.service.generate_alert("TEST_ALERT", "Test message", {"key": "value"})

        assert result["alert_type"] == "TEST_ALERT"
        assert result["message"] == "Test message"
        assert result["email_sent"] is True
        assert result["slack_sent"] is True

    def test_validate_monitoring_rules(self):
        result = self.service.validate_monitoring_rules()

        assert result["total"] == 4
        assert len(result["rules"]) == 4

        for rule in result["rules"]:
            assert rule["valid"] is True
            assert rule["threshold"] > 0
            assert rule["window_minutes"] > 0


@pytest.mark.django_db
class TestSuspiciousActivityDetection:
    def setup_method(self):
        self.service = SecurityMonitoringApplicationService()

    @patch("infrastructure.services.security_monitoring_service.AlertService.send_alert")
    def test_multiple_alert_types(self, mock_send_alert):
        time_now = timezone.now()

        # Create failed logins
        for i in range(6):
            log = AuditLog.objects.create(
                event_type=AuditEventType.LOGIN, user_id="1", success=False
            )
            AuditLog.objects.filter(id=log.id).update(created_at=time_now - timedelta(minutes=i))

        # Create multiple location logins
        for i, ip in enumerate(["192.168.1.1", "10.0.0.1"]):
            log = AuditLog.objects.create(
                event_type=AuditEventType.LOGIN, user_id="1", success=True, ip_address=ip
            )
            AuditLog.objects.filter(id=log.id).update(created_at=time_now - timedelta(minutes=i))

        result = self.service.detect_suspicious_activity("1")

        assert result["suspicious"] is True
        assert len(result["alerts"]) >= 2

    @patch("infrastructure.services.security_monitoring_service.AlertService.send_alert")
    def test_password_reset_spike_detection(self, mock_send_alert):
        time_now = timezone.now()
        for i in range(4):
            log = AuditLog.objects.create(
                event_type=AuditEventType.PASSWORD_RESET, user_id="1", success=True
            )
            AuditLog.objects.filter(id=log.id).update(created_at=time_now - timedelta(minutes=i))

        result = self.service.detect_suspicious_activity("1")

        assert result["suspicious"] is True
        assert "PASSWORD_RESET_SPIKE" in result["alerts"]


@pytest.mark.django_db
class TestAlertGeneration:
    def setup_method(self):
        self.service = SecurityMonitoringApplicationService()

    @patch("infrastructure.services.alert_service.send_mail")
    @patch("infrastructure.services.alert_service.requests.post")
    def test_alert_generation_with_metadata(self, mock_post, mock_send_mail):
        mock_send_mail.return_value = 1
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        self.service.monitoring_service.alert_service.slack_webhook_url = "https://hooks.slack.com/test"

        result = self.service.generate_alert(
            "SECURITY_BREACH", "Potential security breach detected", {"user_id": "1", "severity": "high"}
        )

        assert result["alert_type"] == "SECURITY_BREACH"
        assert result["email_sent"] is True
        assert result["slack_sent"] is True

    @patch("infrastructure.services.alert_service.send_mail", side_effect=Exception("Error"))
    @patch("infrastructure.services.alert_service.requests.post")
    def test_alert_generation_partial_failure(self, mock_post, mock_send_mail):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        self.service.monitoring_service.alert_service.slack_webhook_url = "https://hooks.slack.com/test"

        result = self.service.generate_alert("TEST_ALERT", "Test message")

        assert result["email_sent"] is False
        assert result["slack_sent"] is True


@pytest.mark.django_db
class TestMonitoringRuleValidation:
    def setup_method(self):
        self.service = SecurityMonitoringApplicationService()

    def test_all_rules_valid(self):
        result = self.service.validate_monitoring_rules()

        for rule in result["rules"]:
            assert rule["valid"] is True
            assert rule["threshold"] > 0
            assert rule["window_minutes"] > 0

    def test_rule_configuration(self):
        result = self.service.validate_monitoring_rules()

        alert_types = [rule["alert_type"] for rule in result["rules"]]
        assert "FAILED_LOGIN_SPIKE" in alert_types
        assert "MULTIPLE_LOCATIONS" in alert_types
        assert "PASSWORD_RESET_SPIKE" in alert_types
        assert "ACCOUNT_LOCKOUT_SPIKE" in alert_types
