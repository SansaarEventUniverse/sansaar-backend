import pytest
from domain.models import ABTest, TestVariant
from application.services.ab_testing_service import ABTestingService, VariantManagementService, TestAnalysisService

@pytest.mark.django_db
class TestABTestingService:
    def test_create_test(self):
        """Test creating A/B test"""
        service = ABTestingService()
        test = service.create_test({
            'name': 'Email Subject Test',
            'description': 'Testing different subjects'
        })
        assert test.name == 'Email Subject Test'

    def test_get_tests(self):
        """Test getting A/B tests"""
        ABTest.objects.create(name="Test 1", description="Test 1")
        ABTest.objects.create(name="Test 2", description="Test 2")
        
        service = ABTestingService()
        tests = service.get_tests()
        assert tests.count() == 2

@pytest.mark.django_db
class TestVariantManagementService:
    def test_create_variant(self):
        """Test creating variant"""
        test = ABTest.objects.create(
            name="Test",
            description="Test",
            status="draft"
        )
        
        service = VariantManagementService()
        variant = service.create_variant(test.id, {
            'name': 'Variant A',
            'description': 'Control',
            'traffic_percentage': 50
        })
        assert variant.name == 'Variant A'

@pytest.mark.django_db
class TestTestAnalysisService:
    def test_analyze_test(self):
        """Test analyzing A/B test"""
        test = ABTest.objects.create(
            name="Test",
            description="Test",
            status="running"
        )
        
        service = TestAnalysisService()
        result = service.analyze_test(test.id)
        assert result is not None
