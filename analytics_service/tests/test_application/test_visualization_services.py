import pytest
from domain.models import Visualization, Chart
from application.services.visualization_service import VisualizationService
from application.services.chart_generation_service import ChartGenerationService
from application.services.data_transformation_service import DataTransformationService


@pytest.mark.django_db
class TestVisualizationService:
    def test_create_visualization(self):
        service = VisualizationService()
        viz = service.create_visualization("Test Viz", "dashboard", {"layout": "grid"})
        assert viz.name == "Test Viz"

    def test_get_visualization(self):
        viz = Visualization.objects.create(name="Test", visualization_type="dashboard")
        service = VisualizationService()
        result = service.get_visualization(viz.id)
        assert result.id == viz.id


@pytest.mark.django_db
class TestChartGenerationService:
    def test_generate_chart(self):
        viz = Visualization.objects.create(name="Test", visualization_type="dashboard")
        service = ChartGenerationService()
        chart = service.generate_chart(viz.id, "bar", {"values": [1, 2, 3]})
        assert chart.chart_type == "bar"

    def test_get_chart_data(self):
        viz = Visualization.objects.create(name="Test", visualization_type="dashboard")
        chart = Chart.objects.create(visualization=viz, chart_type="bar", data={"values": [1, 2, 3]})
        service = ChartGenerationService()
        data = service.get_chart_data(chart.id)
        assert data["values"] == [1, 2, 3]


@pytest.mark.django_db
class TestDataTransformationService:
    def test_transform_data(self):
        service = DataTransformationService()
        raw_data = [{"x": 1, "y": 10}, {"x": 2, "y": 20}]
        transformed = service.transform_data(raw_data, "bar")
        assert "values" in transformed

    def test_aggregate_data(self):
        service = DataTransformationService()
        data = [1, 2, 3, 4, 5]
        result = service.aggregate_data(data, "sum")
        assert result == 15
