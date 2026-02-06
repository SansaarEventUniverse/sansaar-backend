import pytest
from infrastructure.repositories.journey_repository import JourneyRepository
from domain.models import CustomerJourney, JourneyStage

@pytest.mark.django_db
class TestJourneyRepository:
    def test_get_journey_stats(self):
        CustomerJourney.objects.create(
            user_id=123,
            campaign_id=1,
            journey_data={'stages': ['awareness']}
        )
        JourneyStage.objects.create(journey_id=1, stage_name='awareness', stage_order=1, stage_data={})
        repo = JourneyRepository()
        stats = repo.get_journey_stats()
        assert stats['total_journeys'] == 1
        assert stats['total_stages'] == 1
