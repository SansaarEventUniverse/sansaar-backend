import pytest
from django.core.exceptions import ValidationError
from domain.models import CustomerJourney, JourneyStage

@pytest.mark.django_db
class TestCustomerJourney:
    def test_create_journey(self):
        journey = CustomerJourney.objects.create(
            user_id=123,
            campaign_id=1,
            journey_data={'start': 'awareness', 'end': 'conversion'},
            status='active'
        )
        assert journey.user_id == 123
        assert journey.status == 'active'

    def test_get_journey_stages(self):
        journey = CustomerJourney.objects.create(
            user_id=123,
            campaign_id=1,
            journey_data={'stages': ['awareness', 'consideration', 'conversion']},
            status='active'
        )
        stages = journey.get_stages()
        assert len(stages) == 3
        assert 'awareness' in stages

    def test_calculate_journey_duration(self):
        journey = CustomerJourney.objects.create(
            user_id=123,
            campaign_id=1,
            journey_data={'duration_days': 7},
            status='completed'
        )
        duration = journey.calculate_duration()
        assert duration == 7

@pytest.mark.django_db
class TestJourneyStage:
    def test_create_stage(self):
        stage = JourneyStage.objects.create(
            journey_id=1,
            stage_name='awareness',
            stage_order=1,
            stage_data={'channel': 'email', 'action': 'open'}
        )
        assert stage.stage_name == 'awareness'
        assert stage.stage_order == 1

    def test_stage_validation(self):
        stage = JourneyStage(
            journey_id=1,
            stage_name='',
            stage_order=1,
            stage_data={}
        )
        with pytest.raises(ValidationError):
            stage.full_clean()

    def test_get_stage_duration(self):
        stage = JourneyStage.objects.create(
            journey_id=1,
            stage_name='consideration',
            stage_order=2,
            stage_data={'duration_hours': 24}
        )
        duration = stage.get_duration()
        assert duration == 24
