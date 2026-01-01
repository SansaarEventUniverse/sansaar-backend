import pytest
from django.utils import timezone
from datetime import timedelta
from domain.models import VolunteerOpportunity, VolunteerApplication
from application.services.application_service import ApplicationService
from application.services.application_workflow_service import ApplicationWorkflowService

@pytest.mark.django_db
class TestApplicationService:
    def test_create_application(self):
        opportunity = VolunteerOpportunity.objects.create(
            title="Event",
            description="Test",
            location="Location",
            start_date=timezone.now() + timedelta(days=5),
            end_date=timezone.now() + timedelta(days=5, hours=3),
            volunteers_needed=10,
            status="open"
        )
        service = ApplicationService()
        data = {
            'opportunity_id': opportunity.id,
            'volunteer_name': 'John Doe',
            'volunteer_email': 'john@example.com',
            'volunteer_phone': '1234567890'
        }
        application = service.create(data)
        assert application.volunteer_name == 'John Doe'
        assert application.status == 'pending'
    
    def test_get_applications_by_opportunity(self):
        opportunity = VolunteerOpportunity.objects.create(
            title="Workshop",
            description="Test",
            location="Location",
            start_date=timezone.now() + timedelta(days=3),
            end_date=timezone.now() + timedelta(days=3, hours=2),
            volunteers_needed=5,
            status="open"
        )
        VolunteerApplication.objects.create(
            opportunity=opportunity,
            volunteer_name="Alice",
            volunteer_email="alice@example.com",
            volunteer_phone="1111111111",
            status="pending"
        )
        service = ApplicationService()
        applications = service.get_by_opportunity(opportunity.id)
        assert applications.count() == 1

@pytest.mark.django_db
class TestApplicationWorkflowService:
    def test_approve_application(self):
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
            volunteer_name="Bob",
            volunteer_email="bob@example.com",
            volunteer_phone="2222222222",
            status="pending"
        )
        service = ApplicationWorkflowService()
        approved = service.approve(application.id)
        assert approved.status == 'approved'
    
    def test_reject_application(self):
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
            volunteer_name="Charlie",
            volunteer_email="charlie@example.com",
            volunteer_phone="3333333333",
            status="pending"
        )
        service = ApplicationWorkflowService()
        rejected = service.reject(application.id)
        assert rejected.status == 'rejected'
