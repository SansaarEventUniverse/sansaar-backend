import pytest
from rest_framework.test import APIClient
from domain.models import Visualization, Chart


@pytest.mark.django_db
class TestVisualizationAPI:
    def test_get_visualization(self):
        viz = Visualization.objects.create(name="Test Viz", visualization_type="dashboard")
        client = APIClient()
        response = client.get(f'/api/analytics/visualizations/{viz.id}/')
        assert response.status_code == 200
        assert response.data['name'] == 'Test Viz'

    def test_create_visualization(self):
        client = APIClient()
        response = client.post('/api/analytics/visualizations/', {
            'name': 'New Viz',
            'visualization_type': 'dashboard',
            'config': {}
        }, format='json')
        assert response.status_code == 201
        assert response.data['name'] == 'New Viz'


@pytest.mark.django_db
class TestChartAPI:
    def test_create_chart(self):
        viz = Visualization.objects.create(name="Test", visualization_type="dashboard")
        client = APIClient()
        response = client.post('/api/analytics/charts/', {
            'visualization_id': viz.id,
            'chart_type': 'bar',
            'data': {'values': [1, 2, 3]},
            'config': {}
        }, format='json')
        assert response.status_code == 201
        assert response.data['chart_type'] == 'bar'

    def test_export_chart(self):
        viz = Visualization.objects.create(name="Test", visualization_type="dashboard")
        chart = Chart.objects.create(visualization=viz, chart_type="bar", data={"values": [1, 2, 3]})
        client = APIClient()
        response = client.get(f'/api/analytics/charts/{chart.id}/export/')
        assert response.status_code == 200
        assert 'chart_type' in response.data
