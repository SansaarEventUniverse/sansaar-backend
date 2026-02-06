import pytest
from application.services.journey_service import CustomerJourneyService, JourneyMappingService, JourneyAnalysisService
from domain.models import CustomerJourney

@pytest.mark.django_db
class TestCustomerJourneyService:
    def test_create_journey(self):
        service = CustomerJourneyService()
        journey = service.create_journey(
            user_id=123,
            campaign_id=1,
            journey_data={'stages': ['awareness', 'consideration']}
        )
        assert journey.user_id == 123
        assert journey.campaign_id == 1

@pytest.mark.django_db
class TestJourneyMappingService:
    def test_map_journey(self):
        service = JourneyMappingService()
        stages = [
            {'name': 'awareness', 'data': {'channel': 'email'}},
            {'name': 'consideration', 'data': {'channel': 'social'}}
        ]
        result = service.map_journey(1, stages)
        assert result['journey_id'] == 1
        assert len(result['stages']) == 2
        assert 'awareness' in result['stages']

@pytest.mark.django_db
class TestJourneyAnalysisService:
    def test_analyze_journey(self):
        CustomerJourney.objects.create(
            user_id=123,
            campaign_id=1,
            journey_data={'stages': ['awareness', 'consideration', 'conversion']}
        )
        service = JourneyAnalysisService()
        result = service.analyze_journey(123)
        assert result['user_id'] == 123
        assert result['total_journeys'] == 1
        assert result['total_stages'] == 3
