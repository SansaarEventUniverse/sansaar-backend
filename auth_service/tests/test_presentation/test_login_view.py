import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from domain.user_model import User


@pytest.mark.django_db
class TestLoginView:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse('login')
        self.user = User.objects.create_user(
            email='test@example.com',
            password='Test@1234',
            first_name='Test',
            last_name='User'
        )
        self.user.verify_email()

    def test_login_success(self):
        data = {
            'email': 'test@example.com',
            'password': 'Test@1234'
        }
        response = self.client.post(self.url, data, format='json')

        assert response.status_code == 200
        assert 'access_token' in response.data
        assert 'refresh_token' in response.data
        assert 'user' in response.data
        assert response.data['user']['email'] == 'test@example.com'

    def test_login_invalid_credentials(self):
        data = {
            'email': 'test@example.com',
            'password': 'WrongPassword'
        }
        response = self.client.post(self.url, data, format='json')

        assert response.status_code == 400
        assert 'error' in response.data

    def test_login_missing_fields(self):
        data = {'email': 'test@example.com'}
        response = self.client.post(self.url, data, format='json')

        assert response.status_code == 400
        assert 'password' in response.data

    def test_login_unverified_email(self):
        User.objects.create_user(
            email='unverified@example.com',
            password='Test@1234',
            first_name='Unverified',
            last_name='User'
        )
        data = {
            'email': 'unverified@example.com',
            'password': 'Test@1234'
        }
        response = self.client.post(self.url, data, format='json')

        assert response.status_code == 400
        assert 'error' in response.data
