import pytest
from rest_framework import status
from rest_framework.test import APIClient

from domain.user_model import User


@pytest.mark.django_db
class TestChangePasswordView:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='OldPassword@123',
            first_name='Test',
            last_name='User',
            is_email_verified=True
        )

    def test_change_password_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/auth/password-change/', {
            'current_password': 'OldPassword@123',
            'new_password': 'NewPassword@456'
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['message'] == 'Password changed successfully'

        self.user.refresh_from_db()
        assert self.user.check_password('NewPassword@456')

    def test_change_password_unauthenticated(self):
        response = self.client.post('/api/auth/password-change/', {
            'current_password': 'OldPassword@123',
            'new_password': 'NewPassword@456'
        })

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_change_password_wrong_current_password(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/auth/password-change/', {
            'current_password': 'WrongPassword@123',
            'new_password': 'NewPassword@456'
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'Current password is incorrect' in str(response.data)

    def test_change_password_weak_new_password(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/auth/password-change/', {
            'current_password': 'OldPassword@123',
            'new_password': 'weak'
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_change_password_missing_fields(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/auth/password-change/', {
            'current_password': 'OldPassword@123'
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
