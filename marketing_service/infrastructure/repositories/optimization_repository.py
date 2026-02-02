from domain.models import CampaignOptimization

class OptimizationRepository:
    def get_optimization_stats(self):
        total = CampaignOptimization.objects.count()
        pending = CampaignOptimization.objects.filter(status='pending').count()
        return {'total_optimizations': total, 'pending_optimizations': pending}
