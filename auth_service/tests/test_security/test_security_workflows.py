import pytest
from django.utils import timezone
from rest_framework.test import APIClient

from domain.backup_code_model import BackupCode
from domain.login_attempt_model import LoginAttempt
from domain.mfa_secret_model import MFASecret
from domain.session_model import Session
from domain.user_model import User


@pytest.mark.django_db
class TestSecurityWorkflows:
    """End-to-end security workflow tests"""
    
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='security@example.com',
            password='Password@123',
            first_name='Security',
            last_name='Test',
            is_email_verified=True
        )

    def test_mfa_bypass_attempt_blocked(self):
        """Test that MFA cannot be bypassed"""
        MFASecret.objects.create(
            user=self.user,
            secret='TESTSECRET123456',
            is_verified=True
        )
        
        response = self.client.post('/api/auth/login/', {
            'email': 'security@example.com',
            'password': 'Password@123'
        })
        
        assert response.status_code == 200
        assert response.json().get('mfa_required') is True
        assert 'access_token' not in response.json()

    def test_lockout_circumvention_blocked(self):
        """Test that lockout cannot be circumvented"""
        for _ in range(5):
            LoginAttempt.objects.create(
                user=self.user,
                ip_address='127.0.0.1',
                success=False
            )
        
        response = self.client.post('/api/auth/login/', {
            'email': 'security@example.com',
            'password': 'Password@123'
        })
        
        assert response.status_code == 429
        assert 'locked' in response.json()['error'].lower()

    def test_session_expiry_enforcement(self):
        """Test that expired sessions are not valid"""
        session = Session.objects.create(
            user=self.user,
            ip_address='127.0.0.1',
            user_agent='Test',
            expires_at=timezone.now() - timezone.timedelta(hours=1)
        )
        
        assert session.is_expired() is True

    def test_concurrent_sessions_management(self):
        """Test managing multiple concurrent sessions"""
        tokens = []
        for _ in range(3):
            response = self.client.post('/api/auth/login/', {
                'email': 'security@example.com',
                'password': 'Password@123'
            })
            tokens.append(response.json()['access_token'])
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens[0]}')
        response = self.client.get('/api/auth/sessions/')
        assert len(response.json()) == 3
        
        response = self.client.delete('/api/auth/sessions/all/')
        assert response.json()['revoked_count'] == 3
