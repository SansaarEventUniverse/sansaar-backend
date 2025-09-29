import pytest
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from domain.password_reset_token_model import PasswordResetToken
from domain.user_model import User


@pytest.mark.django_db
class TestPasswordHistoryAPI:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='Password@123',
            first_name='Test',
            last_name='User',
            is_email_verified=True
        )

    def test_change_password_rejects_recent_password(self):
        # Change password once
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/auth/password-change/', {
            'current_password': 'Password@123',
            'new_password': 'NewPassword@456'
        })
        assert response.status_code == status.HTTP_200_OK

        # Try to change back to old password
        response = self.client.post('/api/auth/password-change/', {
            'current_password': 'NewPassword@456',
            'new_password': 'Password@123'
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'used recently' in str(response.data).lower()

    def test_reset_password_rejects_recent_password(self):
        # Add current password to history
        self.user.add_password_to_history(self.user.password)

        # Create reset token
        token = PasswordResetToken.objects.create(
            user=self.user,
            expires_at=timezone.now() + timezone.timedelta(hours=1)
        )

        # Try to reset to same password
        response = self.client.post('/api/auth/password-reset/confirm/', {
            'token': token.token,
            'new_password': 'Password@123'
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'used recently' in str(response.data).lower()
