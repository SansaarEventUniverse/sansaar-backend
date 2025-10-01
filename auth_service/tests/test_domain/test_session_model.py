import pytest
from django.utils import timezone

from domain.session_model import Session
from domain.user_model import User


@pytest.mark.django_db
class TestSessionModel:
    def setup_method(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='Password@123',
            first_name='Test',
            last_name='User'
        )

    def test_create_session(self):
        session = Session.objects.create(
            user=self.user,
            ip_address='192.168.1.1',
            user_agent='Mozilla/5.0',
            device_type='Desktop',
            browser='Chrome',
            os='Windows'
        )

        assert session.user == self.user
        assert session.ip_address == '192.168.1.1'
        assert session.is_active is True

    def test_session_is_expired(self):
        session = Session.objects.create(
            user=self.user,
            ip_address='192.168.1.1',
            user_agent='Mozilla/5.0'
        )
        
        # Set expiry to past
        session.expires_at = timezone.now() - timezone.timedelta(hours=1)
        session.save()

        assert session.is_expired() is True

    def test_session_not_expired(self):
        session = Session.objects.create(
            user=self.user,
            ip_address='192.168.1.1',
            user_agent='Mozilla/5.0'
        )

        assert session.is_expired() is False

    def test_revoke_session(self):
        session = Session.objects.create(
            user=self.user,
            ip_address='192.168.1.1',
            user_agent='Mozilla/5.0'
        )

        session.revoke()

        assert session.is_active is False
        assert session.revoked_at is not None

    def test_update_last_activity(self):
        session = Session.objects.create(
            user=self.user,
            ip_address='192.168.1.1',
            user_agent='Mozilla/5.0'
        )

        old_activity = session.last_activity_at
        session.update_last_activity()

        assert session.last_activity_at > old_activity

    def test_user_can_have_multiple_sessions(self):
        Session.objects.create(
            user=self.user,
            ip_address='192.168.1.1',
            user_agent='Mozilla/5.0'
        )
        Session.objects.create(
            user=self.user,
            ip_address='192.168.1.2',
            user_agent='Safari'
        )

        assert self.user.sessions.count() == 2
