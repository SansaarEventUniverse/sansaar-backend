import pytest
from unittest.mock import Mock
from django.utils import timezone
from datetime import timedelta
from domain.models import VolunteerOpportunity, VolunteerSkill
from application.services.create_opportunity_service import CreateOpportunityService
from application.services.manage_opportunity_service import ManageOpportunityService
from application.services.skill_matching_service import SkillMatchingService

@pytest.mark.django_db
class TestCreateOpportunityService:
    def test_create_opportunity(self):
        service = CreateOpportunityService()
        data = {
            'title': 'Tree Planting',
            'description': 'Plant trees in the park',
            'location': 'Central Park',
            'start_date': timezone.now() + timedelta(days=5),
            'end_date': timezone.now() + timedelta(days=5, hours=4),
            'volunteers_needed': 15,
            'status': 'open'
        }
        opportunity = service.create(data)
        assert opportunity.title == 'Tree Planting'
        assert opportunity.volunteers_needed == 15
    
    def test_create_opportunity_with_skills(self):
        service = CreateOpportunityService()
        data = {
            'title': 'Coding Workshop',
            'description': 'Teach kids to code',
            'location': 'School',
            'start_date': timezone.now() + timedelta(days=10),
            'end_date': timezone.now() + timedelta(days=10, hours=3),
            'volunteers_needed': 5,
            'status': 'open',
            'skills': [
                {'skill_name': 'Python', 'proficiency_level': 'intermediate', 'is_required': True}
            ]
        }
        opportunity = service.create(data)
        assert opportunity.skills.count() == 1
        assert opportunity.skills.first().skill_name == 'Python'

@pytest.mark.django_db
class TestManageOpportunityService:
    def test_update_opportunity(self):
        opportunity = VolunteerOpportunity.objects.create(
            title='Old Title',
            description='Old description',
            location='Old Location',
            start_date=timezone.now() + timedelta(days=1),
            end_date=timezone.now() + timedelta(days=1, hours=2),
            volunteers_needed=5,
            status='open'
        )
        service = ManageOpportunityService()
        updated = service.update(opportunity.id, {'title': 'New Title'})
        assert updated.title == 'New Title'
    
    def test_close_opportunity(self):
        opportunity = VolunteerOpportunity.objects.create(
            title='Event',
            description='Test event',
            location='Location',
            start_date=timezone.now() + timedelta(days=1),
            end_date=timezone.now() + timedelta(days=1, hours=2),
            volunteers_needed=5,
            status='open'
        )
        service = ManageOpportunityService()
        closed = service.close(opportunity.id)
        assert closed.status == 'closed'

@pytest.mark.django_db
class TestSkillMatchingService:
    def test_match_skills(self):
        opportunity = VolunteerOpportunity.objects.create(
            title='Medical Camp',
            description='Provide medical care',
            location='Rural Area',
            start_date=timezone.now() + timedelta(days=7),
            end_date=timezone.now() + timedelta(days=7, hours=6),
            volunteers_needed=10,
            status='open'
        )
        VolunteerSkill.objects.create(
            opportunity=opportunity,
            skill_name='First Aid',
            proficiency_level='intermediate',
            is_required=True
        )
        service = SkillMatchingService()
        volunteer_skills = ['First Aid', 'CPR']
        match_score = service.calculate_match_score(opportunity.id, volunteer_skills)
        assert match_score > 0
