import pytest
from rest_framework.test import APIClient
from django.utils import timezone
from datetime import timedelta
from domain.models import VolunteerOpportunity, VolunteerSkill

@pytest.mark.django_db
class TestOpportunityAPI:
    def test_create_opportunity(self):
        client = APIClient()
        data = {
            'title': 'Community Garden',
            'description': 'Help maintain community garden',
            'location': 'Downtown',
            'start_date': (timezone.now() + timedelta(days=5)).isoformat(),
            'end_date': (timezone.now() + timedelta(days=5, hours=3)).isoformat(),
            'volunteers_needed': 8,
            'status': 'open'
        }
        response = client.post('/api/volunteering/opportunities/create/', data, format='json')
        assert response.status_code == 201
        assert response.data['title'] == 'Community Garden'
    
    def test_get_opportunities(self):
        VolunteerOpportunity.objects.create(
            title='Event 1',
            description='Test',
            location='Location',
            start_date=timezone.now() + timedelta(days=1),
            end_date=timezone.now() + timedelta(days=1, hours=2),
            volunteers_needed=5,
            status='open'
        )
        client = APIClient()
        response = client.get('/api/volunteering/opportunities/')
        assert response.status_code == 200
        assert len(response.data['results']) == 1
    
    def test_update_opportunity(self):
        opportunity = VolunteerOpportunity.objects.create(
            title='Old Title',
            description='Test',
            location='Location',
            start_date=timezone.now() + timedelta(days=1),
            end_date=timezone.now() + timedelta(days=1, hours=2),
            volunteers_needed=5,
            status='open'
        )
        client = APIClient()
        data = {'title': 'Updated Title'}
        response = client.patch(f'/api/volunteering/opportunities/{opportunity.id}/', data, format='json')
        assert response.status_code == 200
        assert response.data['title'] == 'Updated Title'
    
    def test_create_opportunity_with_skills(self):
        client = APIClient()
        data = {
            'title': 'Workshop',
            'description': 'Teaching workshop',
            'location': 'School',
            'start_date': (timezone.now() + timedelta(days=7)).isoformat(),
            'end_date': (timezone.now() + timedelta(days=7, hours=2)).isoformat(),
            'volunteers_needed': 3,
            'status': 'open',
            'skills': [
                {'skill_name': 'Teaching', 'proficiency_level': 'intermediate', 'is_required': True}
            ]
        }
        response = client.post('/api/volunteering/opportunities/create/', data, format='json')
        assert response.status_code == 201
        assert len(response.data['skills']) == 1
