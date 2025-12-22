import pytest
from rest_framework.test import APIClient
from domain.models import DataExport


@pytest.mark.django_db
class TestDataExportAPI:
    def test_export_data(self):
        client = APIClient()
        response = client.post('/api/analytics/data/export/', {
            'export_name': 'Sales Export',
            'export_format': 'csv',
            'data': {'values': [1, 2, 3]}
        }, format='json')
        assert response.status_code == 201

    def test_schedule_export(self):
        client = APIClient()
        response = client.post('/api/analytics/data/schedule-export/', {
            'export_name': 'Weekly Report',
            'export_format': 'pdf',
            'schedule': 'weekly'
        }, format='json')
        assert response.status_code == 201

    def test_get_export_status(self):
        export = DataExport.objects.create(export_name="Test", export_format="json", status="completed")
        client = APIClient()
        response = client.get(f'/api/analytics/exports/{export.id}/status/')
        assert response.status_code == 200
        assert response.data['status'] == 'completed'
