import pytest
from django.utils import timezone
from datetime import timedelta
from domain.models import VolunteerOpportunity, VolunteerApplication
from infrastructure.repositories.application_repository import ApplicationRepository

@pytest.mark.django_db
class TestApplicationRepository:
    def test_get_pending_applications(self):
        opportunity = VolunteerOpportunity.objects.create(
            title="Event",
            description="Test",
            location="Location",
            start_date=timezone.now() + timedelta(days=1),
            end_date=timezone.now() + timedelta(days=1, hours=2),
            volunteers_needed=5,
            status="open"
        )
        VolunteerApplication.objects.create(
            opportunity=opportunity,
            volunteer_name="John",
            volunteer_email="john@example.com",
            volunteer_phone="1111111111",
            status="pending"
        )
        VolunteerApplication.objects.create(
            opportunity=opportunity,
            volunteer_name="Jane",
            volunteer_email="jane@example.com",
            volunteer_phone="2222222222",
            status="approved"
        )
        repo = ApplicationRepository()
        pending = repo.get_pending_applications()
        assert pending.count() == 1
    
    def test_get_applications_by_status(self):
        opportunity = VolunteerOpportunity.objects.create(
            title="Workshop",
            description="Test",
            location="Location",
            start_date=timezone.now() + timedelta(days=2),
            end_date=timezone.now() + timedelta(days=2, hours=2),
            volunteers_needed=5,
            status="open"
        )
        VolunteerApplication.objects.create(
            opportunity=opportunity,
            volunteer_name="Alice",
            volunteer_email="alice@example.com",
            volunteer_phone="3333333333",
            status="approved"
        )
        VolunteerApplication.objects.create(
            opportunity=opportunity,
            volunteer_name="Bob",
            volunteer_email="bob@example.com",
            volunteer_phone="4444444444",
            status="approved"
        )
        repo = ApplicationRepository()
        approved = repo.get_by_status('approved')
        assert approved.count() == 2
