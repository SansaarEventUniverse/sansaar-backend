import pytest
from domain.models import AudienceSegment, SegmentRule
from application.services.segmentation_service import SegmentationService, AudienceAnalysisService, TargetingService

@pytest.mark.django_db
class TestSegmentationService:
    def test_create_segment(self):
        """Test creating segment"""
        service = SegmentationService()
        segment = service.create_segment({
            'name': 'Premium Users',
            'description': 'Users with premium subscription'
        })
        assert segment.name == 'Premium Users'

    def test_get_segments(self):
        """Test getting segments"""
        AudienceSegment.objects.create(name="Segment 1", description="Test 1")
        AudienceSegment.objects.create(name="Segment 2", description="Test 2")
        
        service = SegmentationService()
        segments = service.get_segments()
        assert segments.count() == 2

@pytest.mark.django_db
class TestAudienceAnalysisService:
    def test_analyze_audience(self):
        """Test analyzing audience"""
        segment = AudienceSegment.objects.create(
            name="Test",
            description="Test segment",
            status="active"
        )
        
        service = AudienceAnalysisService()
        result = service.analyze_audience(segment.id)
        assert result is not None

@pytest.mark.django_db
class TestTargetingService:
    def test_create_targeting_rule(self):
        """Test creating targeting rule"""
        segment = AudienceSegment.objects.create(
            name="Test",
            description="Test",
            status="draft"
        )
        
        service = TargetingService()
        rule = service.create_rule(segment.id, {
            'field': 'age',
            'operator': 'greater_than',
            'value': '25'
        })
        assert rule.field == 'age'
