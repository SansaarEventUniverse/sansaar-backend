import pytest
from domain.models import Visualization, Chart
from infrastructure.rendering.chart_renderer import ChartRenderer
from infrastructure.pipeline.data_transformation_pipeline import DataTransformationPipeline
from infrastructure.cache.visualization_cache import VisualizationCache
from infrastructure.export.chart_exporter import ChartExporter


@pytest.mark.django_db
class TestChartRenderer:
    def test_render_chart(self):
        viz = Visualization.objects.create(name="Test", visualization_type="dashboard")
        chart = Chart.objects.create(visualization=viz, chart_type="bar", data={"values": [1, 2, 3]})
        renderer = ChartRenderer()
        result = renderer.render(chart.id)
        assert "chart_type" in result

    def test_render_with_config(self):
        viz = Visualization.objects.create(name="Test", visualization_type="dashboard")
        chart = Chart.objects.create(
            visualization=viz,
            chart_type="bar",
            data={"values": [1, 2, 3]},
            config={"color": "blue"}
        )
        renderer = ChartRenderer()
        result = renderer.render(chart.id)
        assert result["config"]["color"] == "blue"


@pytest.mark.django_db
class TestDataTransformationPipeline:
    def test_process_data(self):
        pipeline = DataTransformationPipeline()
        data = [{"x": 1, "y": 10}, {"x": 2, "y": 20}]
        result = pipeline.process(data, "bar")
        assert isinstance(result, dict)


@pytest.mark.django_db
class TestVisualizationCache:
    def test_cache_visualization(self):
        viz = Visualization.objects.create(name="Test", visualization_type="dashboard")
        cache = VisualizationCache()
        cache.set(viz.id, {"data": "test"})
        result = cache.get(viz.id)
        assert result["data"] == "test"


@pytest.mark.django_db
class TestChartExporter:
    def test_export_chart(self):
        viz = Visualization.objects.create(name="Test", visualization_type="dashboard")
        chart = Chart.objects.create(visualization=viz, chart_type="bar", data={"values": [1, 2, 3]})
        exporter = ChartExporter()
        result = exporter.export(chart.id, "json")
        assert "chart_type" in result
