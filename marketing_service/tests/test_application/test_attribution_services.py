import pytest
from application.services.attribution_service import AttributionService, TouchPointTrackingService, AttributionAnalysisService
from domain.models import TouchPoint

@pytest.mark.django_db
class TestAttributionService:
    def test_create_attribution(self):
        service = AttributionService()
        attribution = service.create_attribution(
            campaign_id=1,
            model_type='last_click',
            conversion_value=100.0,
            attribution_data={'channel': 'email'}
        )
        assert attribution.campaign_id == 1
        assert attribution.model_type == 'last_click'

@pytest.mark.django_db
class TestTouchPointTrackingService:
    def test_track_touchpoint(self):
        service = TouchPointTrackingService()
        touchpoint = service.track_touchpoint(
            campaign_id=1,
            channel='email',
            user_id=123,
            touchpoint_data={'action': 'click'}
        )
        assert touchpoint.channel == 'email'
        assert touchpoint.user_id == 123

@pytest.mark.django_db
class TestAttributionAnalysisService:
    def test_analyze_attribution(self):
        TouchPoint.objects.create(campaign_id=1, channel='email', user_id=123, touchpoint_data={})
        TouchPoint.objects.create(campaign_id=1, channel='social', user_id=123, touchpoint_data={})
        service = AttributionAnalysisService()
        result = service.analyze_attribution(1)
        assert result['campaign_id'] == 1
        assert result['total_touchpoints'] == 2
        assert len(result['channels']) == 2
