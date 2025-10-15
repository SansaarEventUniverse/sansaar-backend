import pytest
from django.utils import timezone

from application.login_service import LoginService
from domain.login_attempt_model import LoginAttempt
from domain.user_model import User


@pytest.mark.django_db
class TestAccountLockout:
    def setup_method(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="Password@123",
            first_name="Test",
            last_name="User",
            is_email_verified=True,
        )
        self.login_service = LoginService()

    def test_successful_login_resets_attempts(self):
        # Create some failed attempts
        for _ in range(2):
            LoginAttempt.objects.create(user=self.user, ip_address="192.168.1.1", success=False)

        # Successful login
        result = self.login_service.execute(
            email="test@example.com", password="Password@123", ip_address="192.168.1.1", user_agent="test"
        )

        assert result["success"] is True
        assert LoginAttempt.objects.filter(user=self.user).count() == 0

    def test_failed_login_creates_attempt(self):
        result = self.login_service.execute(
            email="test@example.com", password="WrongPassword", ip_address="192.168.1.1", user_agent="test"
        )

        assert result["success"] is False
        assert LoginAttempt.objects.filter(user=self.user, success=False).count() == 1

    def test_account_locked_after_threshold(self):
        # Create 5 failed attempts
        for i in range(5):
            result = self.login_service.execute(
                email="test@example.com", password="WrongPassword", ip_address="192.168.1.1", user_agent="test"
            )
            if i < 4:
                assert result["success"] is False
                assert "locked" not in result.get("error", "").lower()

        # 6th attempt should be locked
        result = self.login_service.execute(
            email="test@example.com",
            password="Password@123",  # Even correct password
            ip_address="192.168.1.1",
            user_agent="test",
        )

        assert result["success"] is False
        assert "locked" in result["error"].lower()

    def test_lockout_expires_after_duration(self):
        # Create 5 failed attempts but old
        old_time = timezone.now() - timezone.timedelta(minutes=20)
        for _ in range(5):
            attempt = LoginAttempt.objects.create(user=self.user, ip_address="192.168.1.1", success=False)
            attempt.created_at = old_time
            attempt.save()

        # Should be able to login now
        result = self.login_service.execute(
            email="test@example.com", password="Password@123", ip_address="192.168.1.1", user_agent="test"
        )

        assert result["success"] is True

    def test_lockout_with_correct_password(self):
        # Create 5 failed attempts
        for _ in range(5):
            LoginAttempt.objects.create(user=self.user, ip_address="192.168.1.1", success=False)

        # Try with correct password - should still be locked
        result = self.login_service.execute(
            email="test@example.com", password="Password@123", ip_address="192.168.1.1", user_agent="test"
        )

        assert result["success"] is False
        assert "locked" in result["error"].lower()
