import pytest
from rest_framework.test import APIClient
from domain.models import AudienceSegment

@pytest.mark.django_db
class TestSegmentationAPI:
    def test_create_segment(self):
        """Test creating segment via API"""
        client = APIClient()
        response = client.post('/api/marketing/audience/segments/', {
            'name': 'Premium Users',
            'description': 'Users with premium subscription'
        }, format='json')
        
        assert response.status_code == 201
        assert response.data['name'] == 'Premium Users'

    def test_list_segments(self):
        """Test listing segments"""
        AudienceSegment.objects.create(name="Segment 1", description="Test 1")
        
        client = APIClient()
        response = client.get('/api/marketing/audience/segments/')
        
        assert response.status_code == 200
        assert len(response.data) == 1

    def test_analyze_audience(self):
        """Test analyzing audience"""
        segment = AudienceSegment.objects.create(
            name="Test",
            description="Test segment",
            status="active"
        )
        
        client = APIClient()
        response = client.post(f'/api/marketing/audience/analyze/', {
            'segment_id': segment.id
        }, format='json')
        
        assert response.status_code == 200
