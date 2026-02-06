import pytest
from django.test import Client
from domain.models import CustomerJourney

@pytest.mark.django_db
class TestJourneyAPI:
    def test_get_customer_journey(self):
        journey = CustomerJourney.objects.create(
            user_id=123,
            campaign_id=1,
            journey_data={'stages': ['awareness', 'consideration']}
        )
        client = Client()
        response = client.get(f'/api/marketing/customer-journey/{journey.id}/')
        assert response.status_code == 200
        assert response.json()['user_id'] == 123

    def test_map_journey(self):
        client = Client()
        response = client.post('/api/marketing/customer-journey/map/', {
            'journey_id': 1,
            'stages': [
                {'name': 'awareness', 'data': {'channel': 'email'}},
                {'name': 'consideration', 'data': {'channel': 'social'}}
            ]
        }, content_type='application/json')
        assert response.status_code == 200
        assert len(response.json()['stages']) == 2

    def test_journey_analysis(self):
        CustomerJourney.objects.create(
            user_id=123,
            campaign_id=1,
            journey_data={'stages': ['awareness', 'consideration', 'conversion']}
        )
        client = Client()
        response = client.get('/api/marketing/customer-journey/analysis/?user_id=123')
        assert response.status_code == 200
        assert response.json()['total_journeys'] == 1
