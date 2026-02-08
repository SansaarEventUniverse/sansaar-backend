import pytest
from django.test import Client
from domain.models import ROIAnalytics

@pytest.mark.django_db
class TestROIAPI:
    def test_calculate_roi(self):
        client = Client()
        response = client.post('/api/marketing/roi/calculate/', {
            'campaign_id': 1,
            'revenue': 10000.0,
            'cost': 2000.0
        }, content_type='application/json')
        assert response.status_code == 200
        assert response.json()['roi'] == 400.0
        assert response.json()['profit'] == 8000.0

    def test_get_roi_analytics(self):
        ROIAnalytics.objects.create(campaign_id=1, revenue=10000.0, cost=2000.0, roi_data={})
        client = Client()
        response = client.get('/api/marketing/roi/?campaign_id=1')
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_roi_report(self):
        ROIAnalytics.objects.create(campaign_id=1, revenue=10000.0, cost=2000.0, roi_data={})
        client = Client()
        response = client.get('/api/marketing/roi/report/?campaign_id=1')
        assert response.status_code == 200
        assert response.json()['roi'] == 400.0
