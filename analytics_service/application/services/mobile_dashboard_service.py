from domain.models import MobileDashboard


class MobileDashboardService:
    def create_dashboard(self, name: str, layout: str):
        return MobileDashboard.objects.create(
            name=name,
            layout=layout,
            is_optimized=True
        )

    def get_dashboard(self, dashboard_id: int):
        return MobileDashboard.objects.get(id=dashboard_id)
