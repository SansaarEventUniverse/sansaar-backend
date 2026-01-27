import pytest
from rest_framework.test import APIClient
from domain.models import ABTest

@pytest.mark.django_db
class TestABTestingAPI:
    def test_create_ab_test(self):
        """Test creating A/B test via API"""
        client = APIClient()
        response = client.post('/api/marketing/ab-tests/', {
            'name': 'Email Subject Test',
            'description': 'Testing different email subjects'
        }, format='json')
        
        assert response.status_code == 201
        assert response.data['name'] == 'Email Subject Test'

    def test_list_ab_tests(self):
        """Test listing A/B tests"""
        ABTest.objects.create(name="Test 1", description="Test 1")
        
        client = APIClient()
        response = client.get('/api/marketing/ab-tests/')
        
        assert response.status_code == 200
        assert len(response.data) == 1

    def test_run_ab_test(self):
        """Test running A/B test"""
        test = ABTest.objects.create(
            name="Test",
            description="Test",
            status="draft"
        )
        
        client = APIClient()
        response = client.post(f'/api/marketing/ab-tests/{test.id}/run/', format='json')
        
        assert response.status_code == 200
