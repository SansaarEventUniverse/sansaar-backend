import pytest
from rest_framework.test import APIClient
from django.utils import timezone
from datetime import timedelta
from domain.models import VolunteerOpportunity, VolunteerApplication

@pytest.mark.django_db
class TestApplicationAPI:
    def test_apply_for_opportunity(self):
        opportunity = VolunteerOpportunity.objects.create(
            title="Beach Cleanup",
            description="Clean the beach",
            location="Beach",
            start_date=timezone.now() + timedelta(days=5),
            end_date=timezone.now() + timedelta(days=5, hours=3),
            volunteers_needed=10,
            status="open"
        )
        client = APIClient()
        data = {
            'volunteer_name': 'John Doe',
            'volunteer_email': 'john@example.com',
            'volunteer_phone': '1234567890'
        }
        response = client.post(f'/api/volunteering/opportunities/{opportunity.id}/apply/', data, format='json')
        assert response.status_code == 201
        assert response.data['volunteer_name'] == 'John Doe'
        assert response.data['status'] == 'pending'
    
    def test_get_all_applications(self):
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
            volunteer_name="Alice",
            volunteer_email="alice@example.com",
            volunteer_phone="1111111111",
            status="pending"
        )
        client = APIClient()
        response = client.get('/api/volunteering/applications/')
        assert response.status_code == 200
        assert len(response.data['results']) == 1
    
    def test_update_application_status(self):
        opportunity = VolunteerOpportunity.objects.create(
            title="Workshop",
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
        client = APIClient()
        data = {'status': 'approved'}
        response = client.patch(f'/api/volunteering/applications/{application.id}/', data, format='json')
        assert response.status_code == 200
        assert response.data['status'] == 'approved'
