from domain.models import MobileDashboard


class MobileOptimizer:
    def optimize(self, dashboard_id: int):
        dashboard = MobileDashboard.objects.get(id=dashboard_id)
        dashboard.is_optimized = True
        dashboard.save()
        return dashboard
