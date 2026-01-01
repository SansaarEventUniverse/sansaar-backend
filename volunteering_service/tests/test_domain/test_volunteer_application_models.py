import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from domain.models import VolunteerOpportunity, VolunteerApplication

@pytest.mark.django_db
class TestVolunteerApplication:
    def test_create_application(self):
        opportunity = VolunteerOpportunity.objects.create(
            title="Beach Cleanup",
            description="Clean the beach",
            location="Beach",
            start_date=timezone.now() + timedelta(days=7),
            end_date=timezone.now() + timedelta(days=7, hours=4),
            volunteers_needed=10,
            status="open"
        )
        application = VolunteerApplication.objects.create(
            opportunity=opportunity,
            volunteer_name="John Doe",
            volunteer_email="john@example.com",
            volunteer_phone="1234567890",
            status="pending"
        )
        assert application.volunteer_name == "John Doe"
        assert application.status == "pending"
    
    def test_application_is_pending(self):
        opportunity = VolunteerOpportunity.objects.create(
            title="Event",
            description="Test",
            location="Location",
            start_date=timezone.now() + timedelta(days=1),
            end_date=timezone.now() + timedelta(days=1, hours=2),
            volunteers_needed=5,
            status="open"
        )
        application = VolunteerApplication.objects.create(
            opportunity=opportunity,
            volunteer_name="Jane Doe",
            volunteer_email="jane@example.com",
            volunteer_phone="0987654321",
            status="pending"
        )
        assert application.is_pending() is True
    
    def test_application_approve(self):
        opportunity = VolunteerOpportunity.objects.create(
            title="Workshop",
            description="Test",
            location="Location",
            start_date=timezone.now() + timedelta(days=3),
            end_date=timezone.now() + timedelta(days=3, hours=2),
            volunteers_needed=5,
            status="open"
        )
        application = VolunteerApplication.objects.create(
            opportunity=opportunity,
            volunteer_name="Bob Smith",
            volunteer_email="bob@example.com",
            volunteer_phone="1112223333",
            status="pending"
        )
        application.approve()
        assert application.status == "approved"
    
    def test_application_reject(self):
        opportunity = VolunteerOpportunity.objects.create(
            title="Event",
            description="Test",
            location="Location",
            start_date=timezone.now() + timedelta(days=2),
            end_date=timezone.now() + timedelta(days=2, hours=2),
            volunteers_needed=5,
            status="open"
        )
        application = VolunteerApplication.objects.create(
            opportunity=opportunity,
            volunteer_name="Alice Brown",
            volunteer_email="alice@example.com",
            volunteer_phone="4445556666",
            status="pending"
        )
        application.reject()
        assert application.status == "rejected"
    
    def test_application_belongs_to_opportunity(self):
        opportunity = VolunteerOpportunity.objects.create(
            title="Community Service",
            description="Help community",
            location="Community Center",
            start_date=timezone.now() + timedelta(days=5),
            end_date=timezone.now() + timedelta(days=5, hours=3),
            volunteers_needed=8,
            status="open"
        )
        application = VolunteerApplication.objects.create(
            opportunity=opportunity,
            volunteer_name="Charlie Wilson",
            volunteer_email="charlie@example.com",
            volunteer_phone="7778889999",
            status="pending"
        )
        assert application.opportunity == opportunity
        assert opportunity.applications.count() == 1
