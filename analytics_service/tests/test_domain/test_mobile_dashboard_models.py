import pytest
from domain.models import MobileDashboard, MobileWidget


@pytest.mark.django_db
class TestMobileDashboardModel:
    def test_create_mobile_dashboard(self):
        dashboard = MobileDashboard.objects.create(
            name="Mobile Analytics",
            layout="compact",
            is_optimized=True
        )
        assert dashboard.name == "Mobile Analytics"
        assert dashboard.is_optimized is True

    def test_is_responsive(self):
        dashboard = MobileDashboard.objects.create(
            name="Responsive Dashboard",
            layout="responsive",
            is_optimized=True
        )
        assert dashboard.is_responsive() is True


@pytest.mark.django_db
class TestMobileWidgetModel:
    def test_create_mobile_widget(self):
        dashboard = MobileDashboard.objects.create(name="Test", layout="compact", is_optimized=True)
        widget = MobileWidget.objects.create(
            dashboard=dashboard,
            widget_type="chart",
            size="small",
            position=1
        )
        assert widget.widget_type == "chart"
        assert widget.size == "small"

    def test_is_compact(self):
        dashboard = MobileDashboard.objects.create(name="Test", layout="compact", is_optimized=True)
        widget = MobileWidget.objects.create(
            dashboard=dashboard,
            widget_type="metric",
            size="small",
            position=1
        )
        assert widget.is_compact() is True
