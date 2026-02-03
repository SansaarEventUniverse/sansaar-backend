import pytest
from django.test import Client
from domain.models import CampaignOptimization, OptimizationRule

@pytest.mark.django_db
class TestOptimizationAPI:
    def test_optimize_campaign(self):
        client = Client()
        response = client.post('/api/marketing/campaigns/1/optimize/', {
            'optimization_type': 'budget',
            'current_metrics': {'ctr': 2.0},
            'target_metrics': {'ctr': 3.0}
        }, content_type='application/json')
        assert response.status_code == 200
        assert response.json()['status'] == 'applied'

    def test_get_optimization(self):
        CampaignOptimization.objects.create(
            campaign_id=1,
            optimization_type='budget',
            current_metrics={'ctr': 2.0},
            target_metrics={'ctr': 3.0}
        )
        client = Client()
        response = client.get('/api/marketing/campaigns/1/optimization/')
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_auto_optimize(self):
        OptimizationRule.objects.create(
            name='Test Rule',
            rule_type='performance',
            conditions={'min_ctr': 2.0},
            actions={'adjust': True}
        )
        client = Client()
        response = client.post('/api/marketing/campaigns/1/auto-optimize/', {
            'metrics': {'ctr': 2.5}
        }, content_type='application/json')
        assert response.status_code == 200
        assert 'applied_rules' in response.json()
