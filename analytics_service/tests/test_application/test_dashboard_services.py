import pytest
from application.services.dashboard_service import DashboardService
from application.services.widget_management_service import WidgetManagementService
from application.services.dashboard_analytics_service import DashboardAnalyticsService
from domain.models import Dashboard, DashboardWidget, AnalyticsEvent


@pytest.mark.django_db
class TestDashboardService:
    def test_create_dashboard(self):
        service = DashboardService()
        dashboard = service.create_dashboard('org_123', 'My Dashboard', {'columns': 3})
        assert dashboard.organizer_id == 'org_123'
        assert dashboard.name == 'My Dashboard'

    def test_get_organizer_dashboards(self):
        service = DashboardService()
        service.create_dashboard('org_123', 'Dashboard 1')
        service.create_dashboard('org_123', 'Dashboard 2')
        dashboards = service.get_organizer_dashboards('org_123')
        assert dashboards.count() == 2

    def test_update_dashboard_layout(self):
        service = DashboardService()
        dashboard = service.create_dashboard('org_123', 'Test')
        updated = service.update_dashboard_layout(dashboard.id, {'columns': 4})
        assert updated.layout['columns'] == 4


@pytest.mark.django_db
class TestWidgetManagementService:
    def test_add_widget(self):
        service = WidgetManagementService()
        dashboard = Dashboard.objects.create(organizer_id='org_123', name='Test')
        widget = service.add_widget(dashboard.id, 'chart', 'Sales Chart', {'type': 'bar'})
        assert widget.widget_type == 'chart'
        assert widget.title == 'Sales Chart'

    def test_remove_widget(self):
        service = WidgetManagementService()
        dashboard = Dashboard.objects.create(organizer_id='org_123', name='Test')
        widget = DashboardWidget.objects.create(dashboard=dashboard, widget_type='chart', title='Test')
        service.remove_widget(widget.id)
        assert DashboardWidget.objects.filter(id=widget.id).count() == 0

    def test_reorder_widgets(self):
        service = WidgetManagementService()
        dashboard = Dashboard.objects.create(organizer_id='org_123', name='Test')
        w1 = DashboardWidget.objects.create(dashboard=dashboard, widget_type='chart', title='W1', position=1)
        w2 = DashboardWidget.objects.create(dashboard=dashboard, widget_type='table', title='W2', position=2)
        service.reorder_widgets([w2.id, w1.id])
        w1.refresh_from_db()
        w2.refresh_from_db()
        assert w2.position == 1
        assert w1.position == 2


@pytest.mark.django_db
class TestDashboardAnalyticsService:
    def test_get_dashboard_data(self):
        service = DashboardAnalyticsService()
        AnalyticsEvent.objects.create(event_type='page_view', event_data={})
        AnalyticsEvent.objects.create(event_type='click', event_data={})
        data = service.get_dashboard_data('org_123')
        assert 'total_events' in data
        assert data['total_events'] >= 2

    def test_get_widget_data(self):
        service = DashboardAnalyticsService()
        dashboard = Dashboard.objects.create(organizer_id='org_123', name='Test')
        widget = DashboardWidget.objects.create(
            dashboard=dashboard,
            widget_type='chart',
            title='Test',
            config={'metric': 'total_events'}
        )
        data = service.get_widget_data(widget.id)
        assert data is not None
