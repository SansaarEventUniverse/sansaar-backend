from datetime import timedelta
from unittest.mock import MagicMock, patch

import pytest
from django.utils import timezone

from domain.audit_log_model import AuditEventType
from domain.models import AuditLog
from infrastructure.alert_thresholds import AlertThresholds
from infrastructure.services.alert_service import AlertService
from infrastructure.services.security_monitoring_service import SecurityMonitoringService


@pytest.mark.django_db
class TestAlertService:
    def setup_method(self):
        self.service = AlertService()

    @patch("infrastructure.services.alert_service.send_mail")
    def test_send_email_alert_success(self, mock_send_mail):
        mock_send_mail.return_value = 1

        result = self.service._send_email_alert("TEST_ALERT", "Test message", {"key": "value"})

        assert result is True
        mock_send_mail.assert_called_once()

    @patch("infrastructure.services.alert_service.send_mail", side_effect=Exception("Email error"))
    def test_send_email_alert_failure(self, mock_send_mail):
        result = self.service._send_email_alert("TEST_ALERT", "Test message")
        assert result is False

    @patch("infrastructure.services.alert_service.requests.post")
    def test_send_slack_alert_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        service = AlertService()
        service.slack_webhook_url = "https://hooks.slack.com/test"

        result = service._send_slack_alert("TEST_ALERT", "Test message", {"key": "value"})

        assert result is True
        mock_post.assert_called_once()

    @patch("infrastructure.services.alert_service.requests.post")
    def test_send_slack_alert_no_webhook(self, mock_post):
        service = AlertService()
        service.slack_webhook_url = ""

        result = service._send_slack_alert("TEST_ALERT", "Test message")

        assert result is False
        mock_post.assert_not_called()

    @patch("infrastructure.services.alert_service.requests.post", side_effect=Exception("Slack error"))
    def test_send_slack_alert_failure(self, mock_post):
        service = AlertService()
        service.slack_webhook_url = "https://hooks.slack.com/test"

        result = service._send_slack_alert("TEST_ALERT", "Test message")

        assert result is False

    @patch.object(AlertService, "_send_email_alert", return_value=True)
    @patch.object(AlertService, "_send_slack_alert", return_value=True)
    def test_send_alert(self, mock_slack, mock_email):
        result = self.service.send_alert("TEST_ALERT", "Test message", {"key": "value"})

        assert result["email_sent"] is True
        assert result["slack_sent"] is True


@pytest.mark.django_db
class TestSecurityMonitoring:
    def setup_method(self):
        self.service = SecurityMonitoringService()

    @patch.object(AlertService, "send_alert")
    def test_monitor_failed_logins_triggers_alert(self, mock_send_alert):
        time_now = timezone.now()
        for i in range(6):
            log = AuditLog.objects.create(
                event_type=AuditEventType.LOGIN, user_id="1", success=False
            )
            AuditLog.objects.filter(id=log.id).update(created_at=time_now - timedelta(minutes=i))

        result = self.service.monitor_failed_logins("1")

        assert result is True
        mock_send_alert.assert_called_once()

    @patch.object(AlertService, "send_alert")
    def test_monitor_failed_logins_no_alert(self, mock_send_alert):
        for i in range(3):
            AuditLog.objects.create(
                event_type=AuditEventType.LOGIN, user_id="1", success=False
            )

        result = self.service.monitor_failed_logins("1")

        assert result is False
        mock_send_alert.assert_not_called()

    @patch.object(AlertService, "send_alert")
    def test_monitor_multiple_locations_triggers_alert(self, mock_send_alert):
        time_now = timezone.now()
        ips = ["192.168.1.1", "10.0.0.1"]

        for i, ip in enumerate(ips):
            log = AuditLog.objects.create(
                event_type=AuditEventType.LOGIN, user_id="1", success=True, ip_address=ip
            )
            AuditLog.objects.filter(id=log.id).update(created_at=time_now - timedelta(minutes=i))

        result = self.service.monitor_multiple_locations("1")

        assert result is True
        mock_send_alert.assert_called_once()

    @patch.object(AlertService, "send_alert")
    def test_monitor_multiple_locations_no_alert(self, mock_send_alert):
        AuditLog.objects.create(
            event_type=AuditEventType.LOGIN, user_id="1", success=True, ip_address="192.168.1.1"
        )

        result = self.service.monitor_multiple_locations("1")

        assert result is False
        mock_send_alert.assert_not_called()

    @patch.object(AlertService, "send_alert")
    def test_monitor_password_reset_attempts_triggers_alert(self, mock_send_alert):
        time_now = timezone.now()
        for i in range(4):
            log = AuditLog.objects.create(
                event_type=AuditEventType.PASSWORD_RESET, user_id="1", success=True
            )
            AuditLog.objects.filter(id=log.id).update(created_at=time_now - timedelta(minutes=i))

        result = self.service.monitor_password_reset_attempts("1")

        assert result is True
        mock_send_alert.assert_called_once()

    @patch.object(AlertService, "send_alert")
    def test_monitor_account_lockouts_triggers_alert(self, mock_send_alert):
        time_now = timezone.now()
        for i in range(11):
            log = AuditLog.objects.create(
                event_type=AuditEventType.ACCOUNT_LOCKED, user_id=str(i), success=True
            )
            AuditLog.objects.filter(id=log.id).update(created_at=time_now - timedelta(minutes=i))

        result = self.service.monitor_account_lockouts()

        assert result is True
        mock_send_alert.assert_called_once()


@pytest.mark.django_db
class TestAlertThresholds:
    def test_get_threshold_failed_login(self):
        config = AlertThresholds.get_threshold("FAILED_LOGIN_SPIKE")
        assert config["threshold"] == 5
        assert config["window_minutes"] == 15

    def test_get_threshold_multiple_locations(self):
        config = AlertThresholds.get_threshold("MULTIPLE_LOCATIONS")
        assert config["threshold"] == 2
        assert config["window_minutes"] == 30

    def test_get_threshold_unknown(self):
        config = AlertThresholds.get_threshold("UNKNOWN_ALERT")
        assert config["threshold"] == 5
        assert config["window_minutes"] == 15


@pytest.mark.django_db
class TestNotificationDelivery:
    @patch("infrastructure.services.alert_service.send_mail")
    @patch("infrastructure.services.alert_service.requests.post")
    def test_notification_delivery_both_channels(self, mock_post, mock_send_mail):
        mock_send_mail.return_value = 1
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        service = AlertService()
        service.slack_webhook_url = "https://hooks.slack.com/test"

        result = service.send_alert("TEST_ALERT", "Test message", {"key": "value"})

        assert result["email_sent"] is True
        assert result["slack_sent"] is True

    @patch("infrastructure.services.alert_service.send_mail", side_effect=Exception("Error"))
    @patch("infrastructure.services.alert_service.requests.post")
    def test_notification_delivery_partial_failure(self, mock_post, mock_send_mail):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        service = AlertService()
        service.slack_webhook_url = "https://hooks.slack.com/test"

        result = service.send_alert("TEST_ALERT", "Test message")

        assert result["email_sent"] is False
        assert result["slack_sent"] is True
