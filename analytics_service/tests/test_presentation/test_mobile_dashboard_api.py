import pytest
from rest_framework.test import APIClient
from domain.models import MobileDashboard, MobileWidget


@pytest.mark.django_db
class TestMobileDashboardAPI:
    def test_get_mobile_dashboard(self):
        dashboard = MobileDashboard.objects.create(name="Mobile Analytics", layout="compact", is_optimized=True)
        client = APIClient()
        response = client.get(f'/api/analytics/mobile/dashboard/{dashboard.id}/')
        assert response.status_code == 200

    def test_mobile_widgets(self):
        dashboard = MobileDashboard.objects.create(name="Test", layout="compact", is_optimized=True)
        MobileWidget.objects.create(dashboard=dashboard, widget_type="chart", size="small", position=1)
        client = APIClient()
        response = client.get(f'/api/analytics/mobile/widgets/?dashboard_id={dashboard.id}')
        assert response.status_code == 200
