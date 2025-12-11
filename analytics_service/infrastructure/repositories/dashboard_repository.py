from domain.models import Dashboard


class DashboardRepository:
    def save_dashboard(self, organizer_id, name, layout=None):
        return Dashboard.objects.create(
            organizer_id=organizer_id,
            name=name,
            layout=layout or {}
        )

    def get_dashboard_by_id(self, dashboard_id):
        return Dashboard.objects.get(id=dashboard_id)

    def get_dashboards_by_organizer(self, organizer_id):
        return Dashboard.objects.filter(organizer_id=organizer_id)
