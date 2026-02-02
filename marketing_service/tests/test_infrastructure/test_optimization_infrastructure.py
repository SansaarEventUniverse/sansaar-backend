import pytest
from infrastructure.repositories.optimization_repository import OptimizationRepository
from domain.models import CampaignOptimization

@pytest.mark.django_db
class TestOptimizationRepository:
    def test_get_optimization_stats(self):
        CampaignOptimization.objects.create(
            campaign_id=1,
            optimization_type='budget',
            current_metrics={'ctr': 2.0},
            target_metrics={'ctr': 3.0},
            status='pending'
        )
        repo = OptimizationRepository()
        stats = repo.get_optimization_stats()
        assert stats['total_optimizations'] == 1
        assert stats['pending_optimizations'] == 1
