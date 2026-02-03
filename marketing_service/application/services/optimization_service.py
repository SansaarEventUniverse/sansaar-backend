from domain.models import CampaignOptimization, OptimizationRule

class CampaignOptimizationService:
    def optimize_campaign(self, campaign_id, optimization_type, current_metrics, target_metrics):
        optimization = CampaignOptimization.objects.create(
            campaign_id=campaign_id,
            optimization_type=optimization_type,
            current_metrics=current_metrics,
            target_metrics=target_metrics
        )
        return optimization.apply_optimization()

class AutoOptimizationService:
    def auto_optimize(self, campaign_id, metrics):
        rules = OptimizationRule.objects.filter(is_active=True)
        applied_rules = []
        for rule in rules:
            if rule.evaluate(metrics):
                applied_rules.append(rule.name)
        return {'campaign_id': campaign_id, 'applied_rules': applied_rules}

class PerformanceOptimizationService:
    def optimize_performance(self, campaign_id, metrics):
        improvement = 0
        if metrics.get('ctr', 0) < 2.0:
            improvement = 25
        return {'campaign_id': campaign_id, 'improvement_percentage': improvement}
