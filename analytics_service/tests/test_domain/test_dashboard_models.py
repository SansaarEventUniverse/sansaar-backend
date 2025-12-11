import pytest
from django.core.exceptions import ValidationError
from domain.models import Dashboard, DashboardWidget


@pytest.mark.django_db
class TestDashboard:
    def test_create_dashboard(self):
        dashboard = Dashboard.objects.create(
            organizer_id='org_123',
            name='My Dashboard',
            layout={'columns': 3}
        )
        assert dashboard.organizer_id == 'org_123'
        assert dashboard.is_active is True

    def test_organizer_id_validation(self):
        dashboard = Dashboard(organizer_id='', name='Test')
        with pytest.raises(ValidationError):
            dashboard.full_clean()

    def test_activate_dashboard(self):
        dashboard = Dashboard.objects.create(organizer_id='org_123', name='Test', is_active=False)
        dashboard.activate()
        assert dashboard.is_active is True

    def test_deactivate_dashboard(self):
        dashboard = Dashboard.objects.create(organizer_id='org_123', name='Test')
        dashboard.deactivate()
        assert dashboard.is_active is False

    def test_get_active_dashboards(self):
        Dashboard.objects.create(organizer_id='org_123', name='Active')
        Dashboard.objects.create(organizer_id='org_123', name='Inactive', is_active=False)
        assert Dashboard.get_active_dashboards('org_123').count() == 1


@pytest.mark.django_db
class TestDashboardWidget:
    def test_create_widget(self):
        dashboard = Dashboard.objects.create(organizer_id='org_123', name='Test')
        widget = DashboardWidget.objects.create(
            dashboard=dashboard,
            widget_type='chart',
            title='Sales Chart',
            config={'chart_type': 'bar'},
            position=1
        )
        assert widget.widget_type == 'chart'
        assert widget.is_visible is True

    def test_widget_type_validation(self):
        dashboard = Dashboard.objects.create(organizer_id='org_123', name='Test')
        widget = DashboardWidget(dashboard=dashboard, widget_type='', title='Test')
        with pytest.raises(ValidationError):
            widget.full_clean()

    def test_toggle_visibility(self):
        dashboard = Dashboard.objects.create(organizer_id='org_123', name='Test')
        widget = DashboardWidget.objects.create(
            dashboard=dashboard,
            widget_type='chart',
            title='Test'
        )
        widget.toggle_visibility()
        assert widget.is_visible is False
        widget.toggle_visibility()
        assert widget.is_visible is True

    def test_update_position(self):
        dashboard = Dashboard.objects.create(organizer_id='org_123', name='Test')
        widget = DashboardWidget.objects.create(
            dashboard=dashboard,
            widget_type='chart',
            title='Test',
            position=1
        )
        widget.update_position(5)
        assert widget.position == 5

    def test_get_visible_widgets(self):
        dashboard = Dashboard.objects.create(organizer_id='org_123', name='Test')
        DashboardWidget.objects.create(dashboard=dashboard, widget_type='chart', title='Visible')
        DashboardWidget.objects.create(dashboard=dashboard, widget_type='table', title='Hidden', is_visible=False)
        assert DashboardWidget.get_visible_widgets(dashboard).count() == 1
