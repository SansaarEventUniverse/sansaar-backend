import pytest

from domain.audit_log_model import AuditEventType, AuditLog


@pytest.mark.django_db
class TestAuditLogModel:
    def test_create_audit_log(self):
        log = AuditLog.objects.create(
            event_type=AuditEventType.REGISTRATION,
            user_id="123",
            ip_address="192.168.1.1",
            user_agent="Mozilla/5.0",
            metadata={"email": "test@example.com"},
        )

        assert log.event_type == AuditEventType.REGISTRATION
        assert log.user_id == "123"
        assert log.ip_address == "192.168.1.1"
        assert log.success is True

    def test_create_failed_login_log(self):
        log = AuditLog.objects.create(
            event_type=AuditEventType.LOGIN,
            user_id="123",
            ip_address="192.168.1.1",
            success=False,
            metadata={"reason": "Invalid password"},
        )

        assert log.success is False
        assert log.metadata["reason"] == "Invalid password"

    def test_event_type_choices(self):
        assert AuditEventType.REGISTRATION == "REGISTRATION"
        assert AuditEventType.LOGIN == "LOGIN"
        assert AuditEventType.LOGOUT == "LOGOUT"
        assert AuditEventType.EMAIL_VERIFICATION == "EMAIL_VERIFICATION"
        assert AuditEventType.PASSWORD_RESET == "PASSWORD_RESET"
        assert AuditEventType.PASSWORD_CHANGE == "PASSWORD_CHANGE"

    def test_get_event_description(self):
        log = AuditLog.objects.create(event_type=AuditEventType.LOGIN, user_id="123", ip_address="192.168.1.1")

        description = log.get_event_description()
        assert "LOGIN" in description
        assert "123" in description
