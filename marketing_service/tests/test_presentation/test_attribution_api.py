import pytest
from django.test import Client
from domain.models import AttributionModel, TouchPoint

@pytest.mark.django_db
class TestAttributionAPI:
    def test_get_attribution(self):
        attribution = AttributionModel.objects.create(
            campaign_id=1,
            model_type='last_click',
            conversion_value=100.0,
            attribution_data={'channel': 'email'}
        )
        client = Client()
        response = client.get(f'/api/marketing/attribution/{attribution.id}/')
        assert response.status_code == 200
        assert response.json()['model_type'] == 'last_click'

    def test_track_touchpoint(self):
        client = Client()
        response = client.post('/api/marketing/attribution/touchpoint/', {
            'campaign_id': 1,
            'channel': 'email',
            'user_id': 123,
            'touchpoint_data': {'action': 'click'}
        }, content_type='application/json')
        assert response.status_code == 200
        assert response.json()['channel'] == 'email'

    def test_attribution_analysis(self):
        TouchPoint.objects.create(campaign_id=1, channel='email', user_id=123, touchpoint_data={})
        TouchPoint.objects.create(campaign_id=1, channel='social', user_id=123, touchpoint_data={})
        client = Client()
        response = client.get('/api/marketing/attribution/analysis/?campaign_id=1')
        assert response.status_code == 200
        assert response.json()['total_touchpoints'] == 2
