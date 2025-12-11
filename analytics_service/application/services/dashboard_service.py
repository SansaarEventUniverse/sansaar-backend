from domain.models import Dashboard


class DashboardService:
    def create_dashboard(self, organizer_id, name, layout=None):
        return Dashboard.objects.create(
            organizer_id=organizer_id,
            name=name,
            layout=layout or {}
        )

    def get_organizer_dashboards(self, organizer_id):
        return Dashboard.objects.filter(organizer_id=organizer_id)

    def update_dashboard_layout(self, dashboard_id, layout):
        dashboard = Dashboard.objects.get(id=dashboard_id)
        dashboard.layout = layout
        dashboard.save(update_fields=['layout'])
        return dashboard
