import pytest

from application.log_audit_event_service import LogAuditEventService
from domain.audit_log_model import AuditEventType, AuditLog


@pytest.mark.django_db
class TestLogAuditEventService:
    def setup_method(self):
        self.service = LogAuditEventService()

    def test_log_registration_event(self):
        self.service.log_event(
            event_type=AuditEventType.REGISTRATION,
            user_id="123",
            ip_address="192.168.1.1",
            user_agent="Mozilla/5.0",
            metadata={"email": "test@example.com"},
        )

        log = AuditLog.objects.get(user_id="123", event_type=AuditEventType.REGISTRATION)
        assert log.ip_address == "192.168.1.1"
        assert log.metadata["email"] == "test@example.com"

    def test_log_failed_login_event(self):
        self.service.log_event(
            event_type=AuditEventType.LOGIN,
            user_id="123",
            ip_address="192.168.1.1",
            success=False,
            metadata={"reason": "Invalid password"},
        )

        log = AuditLog.objects.get(user_id="123", event_type=AuditEventType.LOGIN)
        assert log.success is False
        assert log.metadata["reason"] == "Invalid password"

    def test_log_event_without_metadata(self):
        self.service.log_event(event_type=AuditEventType.LOGOUT, user_id="123", ip_address="192.168.1.1")

        log = AuditLog.objects.get(user_id="123", event_type=AuditEventType.LOGOUT)
        assert log.metadata == {}
