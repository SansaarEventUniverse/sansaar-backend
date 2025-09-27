import pytest
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from domain.refresh_token_model import RefreshToken
from domain.user_model import User
from infrastructure.services.jwt_service import JWTService


@pytest.mark.django_db
class TestAuthenticationSecurity:
    def setup_method(self):
        self.client = APIClient()
        self.jwt_service = JWTService()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='Password@123',
            first_name='Test',
            last_name='User',
            is_email_verified=True
        )

    def test_login_with_unverified_email(self):
        User.objects.create_user(
            email='unverified@example.com',
            password='Password@123',
            first_name='Test',
            last_name='User',
            is_email_verified=False
        )

        response = self.client.post('/api/auth/login/', {
            'email': 'unverified@example.com',
            'password': 'Password@123'
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'Email not verified' in str(response.data)

    def test_login_with_inactive_account(self):
        self.user.is_active = False
        self.user.save()

        response = self.client.post('/api/auth/login/', {
            'email': 'test@example.com',
            'password': 'Password@123'
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'Account is inactive' in str(response.data)

    def test_token_manipulation_attempt(self):
        # Try to use a manipulated token
        fake_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo5OTk5fQ.fake'

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {fake_token}')
        response = self.client.post('/api/auth/password-change/', {
            'current_password': 'Password@123',
            'new_password': 'NewPassword@456'
        })

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_expired_refresh_token(self):
        RefreshToken.objects.create(
            user=self.user,
            token='expired_token',
            expires_at=timezone.now() - timezone.timedelta(days=1)
        )

        response = self.client.post('/api/auth/logout/', {
            'refresh_token': 'expired_token'
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'Token has expired' in str(response.data)

    def test_blacklisted_token_reuse(self):
        token = RefreshToken.objects.create(
            user=self.user,
            token='test_token',
            expires_at=timezone.now() + timezone.timedelta(days=7)
        )
        token.blacklist()

        response = self.client.post('/api/auth/logout/', {
            'refresh_token': 'test_token'
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'Token already blacklisted' in str(response.data)

    def test_sql_injection_attempt_in_login(self):
        response = self.client.post('/api/auth/login/', {
            'email': "admin' OR '1'='1",
            'password': 'anything'
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_password_requirements_enforcement(self):
        weak_passwords = [
            'short',  # Too short
            'alllowercase123!',  # No uppercase
            'ALLUPPERCASE123!',  # No lowercase
            'NoNumbers!',  # No numbers
            'NoSpecial123',  # No special chars
        ]

        for weak_password in weak_passwords:
            response = self.client.post('/api/auth/register/', {
                'first_name': 'Test',
                'last_name': 'User',
                'email': f'test{weak_password}@example.com',
                'password': weak_password,
                'confirm_password': weak_password,
                'agree_terms': True
            })

            assert response.status_code == status.HTTP_400_BAD_REQUEST
