import pytest
from rest_framework.test import APIClient
from domain.models import CustomReport, ReportTemplate


@pytest.mark.django_db
class TestReportBuilderAPI:
    def test_build_report(self):
        client = APIClient()
        response = client.post('/api/analytics/reports/build/', {
            'name': 'Sales Report',
            'report_type': 'sales',
            'config': {'metrics': ['revenue']}
        }, format='json')
        assert response.status_code == 201
        assert response.data['name'] == 'Sales Report'

    def test_generate_report(self):
        report = CustomReport.objects.create(
            name="Test",
            report_type="sales",
            config={"metrics": ["revenue"]}
        )
        client = APIClient()
        response = client.post(f'/api/analytics/reports/generate/', {
            'report_id': report.id
        }, format='json')
        assert response.status_code == 200
        assert 'report_id' in response.data


@pytest.mark.django_db
class TestReportTemplateAPI:
    def test_save_template(self):
        client = APIClient()
        response = client.post('/api/analytics/report-templates/', {
            'name': 'Monthly Template',
            'template_type': 'monthly',
            'template_config': {'period': 'month'}
        }, format='json')
        assert response.status_code == 201
        assert response.data['name'] == 'Monthly Template'

    def test_get_templates(self):
        ReportTemplate.objects.create(name="T1", template_type="daily", is_active=True)
        client = APIClient()
        response = client.get('/api/analytics/report-templates/')
        assert response.status_code == 200
        assert len(response.data) == 1
