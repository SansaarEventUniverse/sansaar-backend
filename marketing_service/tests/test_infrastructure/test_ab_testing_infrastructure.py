import pytest
from domain.models import ABTest
from infrastructure.repositories.ab_testing_repository import ABTestingRepository

@pytest.mark.django_db
class TestABTestingRepository:
    def test_get_analytics(self):
        """Test getting A/B testing analytics"""
        ABTest.objects.create(name="Test 1", description="Test", status="running")
        ABTest.objects.create(name="Test 2", description="Test", status="completed")
        ABTest.objects.create(name="Test 3", description="Test", status="draft")
        
        repo = ABTestingRepository()
        analytics = repo.get_analytics()
        
        assert analytics['total_tests'] == 3
        assert analytics['running'] == 1
        assert analytics['completed'] == 1
