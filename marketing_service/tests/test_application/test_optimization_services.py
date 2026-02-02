import pytest
from application.services.optimization_service import CampaignOptimizationService, AutoOptimizationService, PerformanceOptimizationService
from domain.models import OptimizationRule

@pytest.mark.django_db
class TestCampaignOptimizationService:
    def test_optimize_campaign(self):
        service = CampaignOptimizationService()
        result = service.optimize_campaign(
            campaign_id=1,
            optimization_type='budget',
            current_metrics={'ctr': 2.0},
            target_metrics={'ctr': 3.0}
        )
        assert result['status'] == 'applied'
        assert 'recommendations' in result

@pytest.mark.django_db
class TestAutoOptimizationService:
    def test_auto_optimize(self):
        OptimizationRule.objects.create(
            name='CTR Rule',
            rule_type='performance',
            conditions={'min_ctr': 2.0},
            actions={'adjust': True}
        )
        service = AutoOptimizationService()
        result = service.auto_optimize(1, {'ctr': 2.5})
        assert result['campaign_id'] == 1
        assert 'CTR Rule' in result['applied_rules']

@pytest.mark.django_db
class TestPerformanceOptimizationService:
    def test_optimize_performance(self):
        service = PerformanceOptimizationService()
        result = service.optimize_performance(1, {'ctr': 1.5})
        assert result['campaign_id'] == 1
        assert result['improvement_percentage'] == 25
