import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from domain.models import VolunteerOpportunity, VolunteerSkill

@pytest.mark.django_db
class TestVolunteerOpportunity:
    def test_create_opportunity(self):
        opportunity = VolunteerOpportunity.objects.create(
            title="Beach Cleanup",
            description="Help clean the beach",
            location="Santa Monica Beach",
            start_date=timezone.now() + timedelta(days=7),
            end_date=timezone.now() + timedelta(days=7, hours=4),
            volunteers_needed=10,
            status="open"
        )
        assert opportunity.title == "Beach Cleanup"
        assert opportunity.volunteers_needed == 10
        assert opportunity.status == "open"
    
    def test_opportunity_is_active(self):
        opportunity = VolunteerOpportunity.objects.create(
            title="Event Setup",
            description="Setup event venue",
            location="Convention Center",
            start_date=timezone.now() + timedelta(days=1),
            end_date=timezone.now() + timedelta(days=1, hours=3),
            volunteers_needed=5,
            status="open"
        )
        assert opportunity.is_active() is True
    
    def test_opportunity_is_full(self):
        opportunity = VolunteerOpportunity.objects.create(
            title="Food Drive",
            description="Distribute food",
            location="Community Center",
            start_date=timezone.now() + timedelta(days=2),
            end_date=timezone.now() + timedelta(days=2, hours=5),
            volunteers_needed=3,
            volunteers_registered=3,
            status="open"
        )
        assert opportunity.is_full() is True
    
    def test_opportunity_end_date_after_start_date(self):
        with pytest.raises(ValidationError):
            opportunity = VolunteerOpportunity(
                title="Invalid Event",
                description="Test",
                location="Test Location",
                start_date=timezone.now() + timedelta(days=1),
                end_date=timezone.now(),
                volunteers_needed=5,
                status="open"
            )
            opportunity.clean()

@pytest.mark.django_db
class TestVolunteerSkill:
    def test_create_skill(self):
        opportunity = VolunteerOpportunity.objects.create(
            title="Tech Workshop",
            description="Teach coding",
            location="Library",
            start_date=timezone.now() + timedelta(days=5),
            end_date=timezone.now() + timedelta(days=5, hours=3),
            volunteers_needed=2,
            status="open"
        )
        skill = VolunteerSkill.objects.create(
            opportunity=opportunity,
            skill_name="Python Programming",
            proficiency_level="intermediate",
            is_required=True
        )
        assert skill.skill_name == "Python Programming"
        assert skill.is_required is True
    
    def test_skill_belongs_to_opportunity(self):
        opportunity = VolunteerOpportunity.objects.create(
            title="Medical Camp",
            description="Provide medical assistance",
            location="Rural Area",
            start_date=timezone.now() + timedelta(days=10),
            end_date=timezone.now() + timedelta(days=10, hours=6),
            volunteers_needed=8,
            status="open"
        )
        skill = VolunteerSkill.objects.create(
            opportunity=opportunity,
            skill_name="First Aid",
            proficiency_level="advanced",
            is_required=True
        )
        assert skill.opportunity == opportunity
        assert opportunity.skills.count() == 1
