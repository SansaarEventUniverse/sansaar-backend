import pytest
from infrastructure.aggregation.dashboard_aggregator import DashboardAggregator
from infrastructure.rendering.widget_renderer import WidgetRenderer
from infrastructure.repositories.dashboard_repository import DashboardRepository
from domain.models import Dashboard, DashboardWidget, AnalyticsEvent


@pytest.mark.django_db
class TestDashboardAggregator:
    def test_aggregate_dashboard_data(self):
        aggregator = DashboardAggregator()
        AnalyticsEvent.objects.create(event_type='page_view', event_data={})
        AnalyticsEvent.objects.create(event_type='click', event_data={})
        data = aggregator.aggregate_dashboard_data('org_123')
        assert 'total_events' in data
        assert data['total_events'] >= 2


@pytest.mark.django_db
class TestWidgetRenderer:
    def test_render_widget(self):
        renderer = WidgetRenderer()
        dashboard = Dashboard.objects.create(organizer_id='org_123', name='Test')
        widget = DashboardWidget.objects.create(
            dashboard=dashboard,
            widget_type='chart',
            title='Test Chart',
            config={'type': 'bar'}
        )
        rendered = renderer.render_widget(widget.id)
        assert 'widget_type' in rendered
        assert rendered['widget_type'] == 'chart'


@pytest.mark.django_db
class TestDashboardRepository:
    def test_save_dashboard(self):
        repo = DashboardRepository()
        dashboard = repo.save_dashboard('org_123', 'My Dashboard', {'columns': 3})
        assert dashboard.id is not None

    def test_get_dashboard_by_id(self):
        repo = DashboardRepository()
        dashboard = Dashboard.objects.create(organizer_id='org_123', name='Test')
        retrieved = repo.get_dashboard_by_id(dashboard.id)
        assert retrieved.id == dashboard.id

    def test_get_dashboards_by_organizer(self):
        repo = DashboardRepository()
        Dashboard.objects.create(organizer_id='org_123', name='D1')
        Dashboard.objects.create(organizer_id='org_123', name='D2')
        dashboards = repo.get_dashboards_by_organizer('org_123')
        assert dashboards.count() == 2
