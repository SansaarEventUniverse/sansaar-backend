import pytest
from rest_framework.test import APIClient
from domain.models import Visualization, CustomReport, DataExport, AuditTrail


@pytest.mark.django_db
class TestVisualizationWorkflowE2E:
    def test_complete_visualization_workflow(self):
        client = APIClient()
        
        # Create visualization
        response = client.post('/api/analytics/visualizations/', {
            'name': 'Sales Dashboard',
            'visualization_type': 'bar',
            'config': {'source': 'sales'}
        }, format='json')
        assert response.status_code == 201
        viz_id = response.data['id']
        
        # Get visualization
        response = client.get(f'/api/analytics/visualizations/{viz_id}/')
        assert response.status_code == 200
        assert response.data['name'] == 'Sales Dashboard'
        
        # Create chart
        response = client.post('/api/analytics/charts/', {
            'visualization_id': viz_id,
            'chart_type': 'bar',
            'data': {'values': [10, 20, 30]}
        }, format='json')
        assert response.status_code == 201


@pytest.mark.django_db
class TestReportingWorkflowE2E:
    def test_complete_reporting_workflow(self):
        client = APIClient()
        
        # Build report
        response = client.post('/api/analytics/reports/build/', {
            'name': 'Monthly Report',
            'report_type': 'monthly',
            'config': {'revenue': 50000}
        }, format='json')
        assert response.status_code == 201
        assert response.data['name'] == 'Monthly Report'


@pytest.mark.django_db
class TestExportWorkflowE2E:
    def test_complete_export_workflow(self):
        # Create export directly
        export = DataExport.objects.create(
            export_name="Monthly Export",
            export_format="csv",
            status="pending"
        )
        
        client = APIClient()
        
        # Check status
        response = client.get(f'/api/analytics/exports/{export.id}/status/')
        assert response.status_code == 200
        assert response.data['status'] == 'pending'


@pytest.mark.django_db
class TestAuditWorkflowE2E:
    def test_complete_audit_workflow(self):
        client = APIClient()
        
        # Create audit trails
        AuditTrail.objects.create(user_id="user-123", action="login", resource="auth")
        AuditTrail.objects.create(user_id="user-123", action="export_data", resource="reports")
        
        # Get audit trail
        response = client.get('/api/analytics/admin/audit-trail/?user_id=user-123')
        assert response.status_code == 200
        assert len(response.data) == 2
        
        # Search audit trail
        response = client.post('/api/analytics/admin/audit/search/', {
            'action': 'login'
        }, format='json')
        assert response.status_code == 200
        assert len(response.data) == 1
        
        # Get compliance
        response = client.get('/api/analytics/admin/compliance/')
        assert response.status_code == 200
