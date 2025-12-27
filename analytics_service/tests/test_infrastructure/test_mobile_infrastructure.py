import pytest
from domain.models import MobileDashboard
from infrastructure.mobile.mobile_optimizer import MobileOptimizer


@pytest.mark.django_db
class TestMobileOptimizer:
    def test_optimize_dashboard(self):
        dashboard = MobileDashboard.objects.create(name="Test", layout="compact", is_optimized=False)
        optimizer = MobileOptimizer()
        optimized = optimizer.optimize(dashboard.id)
        assert optimized.is_optimized is True
