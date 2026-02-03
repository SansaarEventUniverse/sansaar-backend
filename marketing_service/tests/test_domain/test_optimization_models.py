import pytest
from django.core.exceptions import ValidationError
from domain.models import CampaignOptimization, OptimizationRule

@pytest.mark.django_db
class TestCampaignOptimization:
    def test_create_optimization(self):
        optimization = CampaignOptimization.objects.create(
            campaign_id=1,
            optimization_type='budget',
            current_metrics={'ctr': 2.5, 'conversion': 5.0},
            target_metrics={'ctr': 3.0, 'conversion': 6.0}
        )
        assert optimization.campaign_id == 1
        assert optimization.optimization_type == 'budget'
        assert optimization.status == 'pending'

    def test_apply_optimization(self):
        optimization = CampaignOptimization.objects.create(
            campaign_id=1,
            optimization_type='targeting',
            current_metrics={'reach': 1000},
            target_metrics={'reach': 1500}
        )
        result = optimization.apply_optimization()
        assert result['status'] == 'applied'
        assert 'recommendations' in result

    def test_calculate_improvement(self):
        optimization = CampaignOptimization.objects.create(
            campaign_id=1,
            optimization_type='content',
            current_metrics={'engagement': 10.0},
            target_metrics={'engagement': 15.0}
        )
        improvement = optimization.calculate_improvement()
        assert improvement == 50.0

@pytest.mark.django_db
class TestOptimizationRule:
    def test_create_rule(self):
        rule = OptimizationRule.objects.create(
            name='Budget Increase Rule',
            rule_type='budget',
            conditions={'min_roi': 2.0},
            actions={'increase_budget': 20}
        )
        assert rule.name == 'Budget Increase Rule'
        assert rule.is_active is True

    def test_evaluate_rule(self):
        rule = OptimizationRule.objects.create(
            name='CTR Optimization',
            rule_type='performance',
            conditions={'min_ctr': 2.0},
            actions={'adjust_targeting': True}
        )
        metrics = {'ctr': 2.5, 'impressions': 1000}
        result = rule.evaluate(metrics)
        assert result is True

    def test_rule_validation(self):
        rule = OptimizationRule(
            name='',
            rule_type='budget',
            conditions={},
            actions={}
        )
        with pytest.raises(ValidationError):
            rule.full_clean()
