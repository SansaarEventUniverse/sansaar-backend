from domain.models import Dashboard, DashboardWidget


class WidgetManagementService:
    def add_widget(self, dashboard_id, widget_type, title, config=None):
        dashboard = Dashboard.objects.get(id=dashboard_id)
        max_position = DashboardWidget.objects.filter(dashboard=dashboard).count()
        return DashboardWidget.objects.create(
            dashboard=dashboard,
            widget_type=widget_type,
            title=title,
            config=config or {},
            position=max_position + 1
        )

    def remove_widget(self, widget_id):
        DashboardWidget.objects.filter(id=widget_id).delete()

    def reorder_widgets(self, widget_ids):
        for position, widget_id in enumerate(widget_ids, start=1):
            DashboardWidget.objects.filter(id=widget_id).update(position=position)
