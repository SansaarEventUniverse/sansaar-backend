import pytest
from django.utils import timezone

from domain.login_attempt_model import LoginAttempt, LOCKOUT_THRESHOLD, LOCKOUT_DURATION
from domain.user_model import User


@pytest.mark.django_db
class TestLoginAttemptModel:
    def setup_method(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="Password@123", first_name="Test", last_name="User"
        )

    def test_create_login_attempt(self):
        attempt = LoginAttempt.objects.create(user=self.user, ip_address="192.168.1.1", success=False)

        assert attempt.user == self.user
        assert attempt.success is False

    def test_lockout_threshold_constant(self):
        assert LOCKOUT_THRESHOLD == 5

    def test_lockout_duration_constant(self):
        assert LOCKOUT_DURATION == 15  # minutes

    def test_user_is_locked_out(self):
        # Create 5 failed attempts within lockout window
        for _ in range(5):
            LoginAttempt.objects.create(user=self.user, ip_address="192.168.1.1", success=False)

        assert self.user.is_locked_out() is True

    def test_user_not_locked_out_with_fewer_attempts(self):
        # Create only 3 failed attempts
        for _ in range(3):
            LoginAttempt.objects.create(user=self.user, ip_address="192.168.1.1", success=False)

        assert self.user.is_locked_out() is False

    def test_user_not_locked_out_after_duration(self):
        # Create 5 failed attempts but old
        old_time = timezone.now() - timezone.timedelta(minutes=20)
        for _ in range(5):
            attempt = LoginAttempt.objects.create(user=self.user, ip_address="192.168.1.1", success=False)
            attempt.created_at = old_time
            attempt.save()

        assert self.user.is_locked_out() is False

    def test_reset_login_attempts(self):
        # Create failed attempts
        for _ in range(3):
            LoginAttempt.objects.create(user=self.user, ip_address="192.168.1.1", success=False)

        self.user.reset_login_attempts()

        assert LoginAttempt.objects.filter(user=self.user).count() == 0
