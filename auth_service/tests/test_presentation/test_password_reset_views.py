import pytest
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestPasswordResetViews:
    def setup_method(self):
        self.client = APIClient()

    def test_request_password_reset_success(self):
        from domain.user_model import User
        User.objects.create_user(
            email='test@example.com',
            password='Password@123',
            first_name='Test',
            last_name='User',
            is_email_verified=True
        )

        response = self.client.post('/api/auth/password-reset/request/', {
            'email': 'test@example.com'
        })

        assert response.status_code == status.HTTP_200_OK
        assert 'Password reset email sent' in response.data['message']

    def test_request_password_reset_nonexistent_email(self):
        response = self.client.post('/api/auth/password-reset/request/', {
            'email': 'nonexistent@example.com'
        })

        # Should still return 200 for security (don't reveal if email exists)
        assert response.status_code == status.HTTP_200_OK

    def test_reset_password_success(self):
        from django.utils import timezone

        from domain.password_reset_token_model import PasswordResetToken
        from domain.user_model import User

        user = User.objects.create_user(
            email='test@example.com',
            password='OldPassword@123',
            first_name='Test',
            last_name='User',
            is_email_verified=True
        )

        token = PasswordResetToken.objects.create(
            user=user,
            expires_at=timezone.now() + timezone.timedelta(hours=1)
        )

        response = self.client.post('/api/auth/password-reset/confirm/', {
            'token': token.token,
            'new_password': 'NewPassword@456'
        })

        assert response.status_code == status.HTTP_200_OK
        user.refresh_from_db()
        assert user.check_password('NewPassword@456')

    def test_reset_password_invalid_token(self):
        response = self.client.post('/api/auth/password-reset/confirm/', {
            'token': 'invalid_token',
            'new_password': 'NewPassword@456'
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
