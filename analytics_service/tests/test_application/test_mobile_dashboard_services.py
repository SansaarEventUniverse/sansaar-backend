import pytest
from domain.models import MobileDashboard, MobileWidget
from application.services.mobile_dashboard_service import MobileDashboardService


@pytest.mark.django_db
class TestMobileDashboardService:
    def test_create_mobile_dashboard(self):
        service = MobileDashboardService()
        dashboard = service.create_dashboard("Mobile Analytics", "compact")
        assert dashboard.name == "Mobile Analytics"

    def test_get_dashboard(self):
        dashboard = MobileDashboard.objects.create(name="Test", layout="compact", is_optimized=True)
        service = MobileDashboardService()
        result = service.get_dashboard(dashboard.id)
        assert result.id == dashboard.id
