import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
class TestHealthCheck:
    def setup_method(self):
        self.client = APIClient()

    def test_health_check_endpoint(self):
        """Test health check endpoint responds"""
        response = self.client.get('/api/notifications/health/')
        assert response.status_code == 200
        assert 'status' in response.data
        assert 'services' in response.data
