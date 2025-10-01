import pytest

from application.login_service import LoginService
from domain.audit_log_model import AuditEventType, AuditLog
from domain.login_attempt_model import LoginAttempt
from domain.user_model import User


@pytest.mark.django_db
class TestAccountLockoutAudit:
    def setup_method(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='Password@123',
            first_name='Test',
            last_name='User',
            is_email_verified=True
        )
        self.login_service = LoginService()

    def test_account_locked_event_logged(self):
        # Create 5 failed attempts
        for _ in range(5):
            LoginAttempt.objects.create(
                user=self.user,
                ip_address='192.168.1.1',
                success=False
            )

        # Try to login
        self.login_service.execute(
            email='test@example.com',
            password='Password@123',
            ip_address='192.168.1.1',
            user_agent='test'
        )

        # Check audit log
        audit = AuditLog.objects.filter(
            event_type=AuditEventType.ACCOUNT_LOCKED,
            user_id=str(self.user.id)
        ).first()

        assert audit is not None
        assert audit.success is False
        assert 'locked' in audit.metadata['reason'].lower()

    def test_failed_login_logged(self):
        self.login_service.execute(
            email='test@example.com',
            password='WrongPassword',
            ip_address='192.168.1.1',
            user_agent='test'
        )

        # Check audit log
        audit = AuditLog.objects.filter(
            event_type=AuditEventType.LOGIN,
            user_id=str(self.user.id),
            success=False
        ).first()

        assert audit is not None
        assert 'password' in audit.metadata['reason'].lower()
