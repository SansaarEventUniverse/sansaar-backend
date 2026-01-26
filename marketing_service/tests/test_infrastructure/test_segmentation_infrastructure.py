import pytest
from domain.models import AudienceSegment
from infrastructure.repositories.segmentation_repository import SegmentationRepository

@pytest.mark.django_db
class TestSegmentationRepository:
    def test_get_analytics(self):
        """Test getting segmentation analytics"""
        AudienceSegment.objects.create(name="Segment 1", description="Test", status="active")
        AudienceSegment.objects.create(name="Segment 2", description="Test", status="archived")
        AudienceSegment.objects.create(name="Segment 3", description="Test", status="draft")
        
        repo = SegmentationRepository()
        analytics = repo.get_analytics()
        
        assert analytics['total_segments'] == 3
        assert analytics['active'] == 1
        assert analytics['archived'] == 1
