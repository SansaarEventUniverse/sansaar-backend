import pytest
from rest_framework.test import APIClient
from domain.models import Dashboard, DashboardWidget


@pytest.mark.django_db
class TestDashboardAPI:
    def setup_method(self):
        self.client = APIClient()

    def test_get_dashboard(self):
        dashboard = Dashboard.objects.create(organizer_id='org_123', name='My Dashboard')
        response = self.client.get(f'/api/analytics/organizer/dashboard/{dashboard.id}/')
        assert response.status_code == 200
        assert response.data['name'] == 'My Dashboard'

    def test_customize_dashboard(self):
        dashboard = Dashboard.objects.create(organizer_id='org_123', name='Test')
        data = {'layout': {'columns': 4}}
        response = self.client.put(
            f'/api/analytics/organizer/dashboard/{dashboard.id}/customize/',
            data,
            format='json'
        )
        assert response.status_code == 200
        assert response.data['layout']['columns'] == 4

    def test_get_dashboard_widgets(self):
        dashboard = Dashboard.objects.create(organizer_id='org_123', name='Test')
        DashboardWidget.objects.create(dashboard=dashboard, widget_type='chart', title='W1')
        DashboardWidget.objects.create(dashboard=dashboard, widget_type='table', title='W2')
        response = self.client.get(f'/api/analytics/organizer/dashboard/{dashboard.id}/widgets/')
        assert response.status_code == 200
        assert len(response.data) == 2

    def test_create_dashboard(self):
        data = {'organizer_id': 'org_123', 'name': 'New Dashboard', 'layout': {'columns': 3}}
        response = self.client.post('/api/analytics/organizer/dashboard/', data, format='json')
        assert response.status_code == 201
        assert response.data['name'] == 'New Dashboard'

    def test_create_dashboard_missing_name(self):
        data = {'organizer_id': 'org_123'}
        response = self.client.post('/api/analytics/organizer/dashboard/', data, format='json')
        assert response.status_code == 400
        assert 'name' in response.data
