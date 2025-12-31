import pytest
from django.utils import timezone
from datetime import timedelta
from domain.models import VolunteerOpportunity, VolunteerSkill
from infrastructure.repositories.opportunity_repository import OpportunityRepository
from infrastructure.matching.skill_matcher import SkillMatcher

@pytest.mark.django_db
class TestOpportunityRepository:
    def test_get_active_opportunities(self):
        VolunteerOpportunity.objects.create(
            title='Active Event',
            description='Test',
            location='Location',
            start_date=timezone.now() + timedelta(days=1),
            end_date=timezone.now() + timedelta(days=1, hours=2),
            volunteers_needed=5,
            status='open'
        )
        VolunteerOpportunity.objects.create(
            title='Closed Event',
            description='Test',
            location='Location',
            start_date=timezone.now() + timedelta(days=1),
            end_date=timezone.now() + timedelta(days=1, hours=2),
            volunteers_needed=5,
            status='closed'
        )
        repo = OpportunityRepository()
        active = repo.get_active_opportunities()
        assert active.count() == 1
        assert active.first().title == 'Active Event'
    
    def test_get_opportunities_by_location(self):
        VolunteerOpportunity.objects.create(
            title='Event 1',
            description='Test',
            location='New York',
            start_date=timezone.now() + timedelta(days=1),
            end_date=timezone.now() + timedelta(days=1, hours=2),
            volunteers_needed=5,
            status='open'
        )
        VolunteerOpportunity.objects.create(
            title='Event 2',
            description='Test',
            location='Los Angeles',
            start_date=timezone.now() + timedelta(days=1),
            end_date=timezone.now() + timedelta(days=1, hours=2),
            volunteers_needed=5,
            status='open'
        )
        repo = OpportunityRepository()
        ny_opportunities = repo.get_by_location('New York')
        assert ny_opportunities.count() == 1
        assert ny_opportunities.first().location == 'New York'

@pytest.mark.django_db
class TestSkillMatcher:
    def test_find_matching_opportunities(self):
        opp1 = VolunteerOpportunity.objects.create(
            title='Tech Event',
            description='Test',
            location='Location',
            start_date=timezone.now() + timedelta(days=1),
            end_date=timezone.now() + timedelta(days=1, hours=2),
            volunteers_needed=5,
            status='open'
        )
        VolunteerSkill.objects.create(
            opportunity=opp1,
            skill_name='Python',
            proficiency_level='intermediate',
            is_required=True
        )
        opp2 = VolunteerOpportunity.objects.create(
            title='Medical Event',
            description='Test',
            location='Location',
            start_date=timezone.now() + timedelta(days=1),
            end_date=timezone.now() + timedelta(days=1, hours=2),
            volunteers_needed=5,
            status='open'
        )
        VolunteerSkill.objects.create(
            opportunity=opp2,
            skill_name='First Aid',
            proficiency_level='advanced',
            is_required=True
        )
        matcher = SkillMatcher()
        matches = matcher.find_matching_opportunities(['Python', 'JavaScript'])
        assert len(matches) > 0
        assert matches[0]['opportunity'].title == 'Tech Event'
