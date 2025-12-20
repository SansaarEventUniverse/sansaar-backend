import pytest
from django.core.exceptions import ValidationError
from domain.models import Visualization, Chart


@pytest.mark.django_db
class TestVisualization:
    def test_create_visualization(self):
        viz = Visualization.objects.create(
            name="Sales Dashboard",
            visualization_type="dashboard",
            config={"layout": "grid"}
        )
        assert viz.name == "Sales Dashboard"
        assert viz.visualization_type == "dashboard"

    def test_visualization_name_required(self):
        with pytest.raises(ValidationError):
            viz = Visualization(visualization_type="dashboard")
            viz.full_clean()

    def test_get_chart_count(self):
        viz = Visualization.objects.create(
            name="Test Viz",
            visualization_type="dashboard"
        )
        Chart.objects.create(visualization=viz, chart_type="bar", data={})
        Chart.objects.create(visualization=viz, chart_type="line", data={})
        assert viz.get_chart_count() == 2


@pytest.mark.django_db
class TestChart:
    def test_create_chart(self):
        viz = Visualization.objects.create(name="Test", visualization_type="dashboard")
        chart = Chart.objects.create(
            visualization=viz,
            chart_type="bar",
            data={"values": [1, 2, 3]},
            config={"color": "blue"}
        )
        assert chart.chart_type == "bar"
        assert chart.data["values"] == [1, 2, 3]

    def test_chart_type_required(self):
        viz = Visualization.objects.create(name="Test", visualization_type="dashboard")
        with pytest.raises(ValidationError):
            chart = Chart(visualization=viz, data={})
            chart.full_clean()

    def test_validate_chart_data(self):
        viz = Visualization.objects.create(name="Test", visualization_type="dashboard")
        chart = Chart.objects.create(
            visualization=viz,
            chart_type="bar",
            data={"values": [1, 2, 3]}
        )
        assert chart.validate_chart_data() is True
