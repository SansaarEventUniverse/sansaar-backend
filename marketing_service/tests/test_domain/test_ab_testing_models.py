import pytest
from domain.models import ABTest, TestVariant

@pytest.mark.django_db
class TestABTest:
    def test_create_ab_test(self):
        """Test creating A/B test"""
        test = ABTest.objects.create(
            name="Email Subject Test",
            description="Testing different email subjects",
            status="draft"
        )
        assert test.name == "Email Subject Test"
        assert test.status == "draft"

    def test_ab_test_status_choices(self):
        """Test A/B test status validation"""
        test = ABTest.objects.create(
            name="Test",
            description="Test",
            status="running"
        )
        assert test.status in ['draft', 'running', 'completed', 'paused']

    def test_start_test(self):
        """Test starting A/B test"""
        test = ABTest.objects.create(
            name="Test",
            description="Test",
            status="draft"
        )
        test.start()
        assert test.status == "running"

    def test_complete_test(self):
        """Test completing A/B test"""
        test = ABTest.objects.create(
            name="Test",
            description="Test",
            status="running"
        )
        test.complete()
        assert test.status == "completed"

@pytest.mark.django_db
class TestTestVariant:
    def test_create_variant(self):
        """Test creating test variant"""
        test = ABTest.objects.create(
            name="Test",
            description="Test",
            status="draft"
        )
        variant = TestVariant.objects.create(
            ab_test=test,
            name="Variant A",
            description="Control variant",
            traffic_percentage=50
        )
        assert variant.name == "Variant A"
        assert variant.traffic_percentage == 50

    def test_variant_validation(self):
        """Test variant validation"""
        test = ABTest.objects.create(
            name="Test",
            description="Test",
            status="draft"
        )
        variant = TestVariant.objects.create(
            ab_test=test,
            name="Variant B",
            description="Test variant",
            traffic_percentage=50
        )
        assert variant.is_valid()
