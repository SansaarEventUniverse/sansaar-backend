import pytest
from rest_framework.test import APIClient
from domain.models import AutomationWorkflow

@pytest.mark.django_db
class TestAutomationAPI:
    def test_create_workflow(self):
        """Test creating workflow via API"""
        client = APIClient()
        response = client.post('/api/marketing/automation/workflows/', {
            'name': 'Welcome Workflow',
            'trigger_type': 'user_signup'
        }, format='json')
        
        assert response.status_code == 201
        assert response.data['name'] == 'Welcome Workflow'

    def test_list_workflows(self):
        """Test listing workflows"""
        AutomationWorkflow.objects.create(name="Workflow 1", trigger_type="user_signup")
        
        client = APIClient()
        response = client.get('/api/marketing/automation/workflows/')
        
        assert response.status_code == 200
        assert len(response.data) == 1

    def test_execute_workflow(self):
        """Test executing workflow"""
        workflow = AutomationWorkflow.objects.create(
            name="Test",
            trigger_type="user_signup",
            status="active"
        )
        
        client = APIClient()
        response = client.post(f'/api/marketing/automation/workflows/{workflow.id}/execute/', {
            'context': {'user_id': 123}
        }, format='json')
        
        assert response.status_code == 200
