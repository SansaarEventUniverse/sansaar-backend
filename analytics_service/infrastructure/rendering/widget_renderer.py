from domain.models import DashboardWidget


class WidgetRenderer:
    def render_widget(self, widget_id):
        widget = DashboardWidget.objects.get(id=widget_id)
        return {
            'widget_type': widget.widget_type,
            'title': widget.title,
            'config': widget.config,
            'position': widget.position
        }
