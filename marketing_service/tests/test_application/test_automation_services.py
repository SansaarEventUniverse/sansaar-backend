import pytest
from domain.models import AutomationWorkflow, WorkflowTrigger
from application.services.automation_service import AutomationService, WorkflowExecutionService, TriggerManagementService

@pytest.mark.django_db
class TestAutomationService:
    def test_create_workflow(self):
        """Test creating automation workflow"""
        service = AutomationService()
        workflow = service.create_workflow({
            'name': 'Welcome Automation',
            'trigger_type': 'user_signup'
        })
        assert workflow.name == 'Welcome Automation'

    def test_get_workflows(self):
        """Test getting workflows"""
        AutomationWorkflow.objects.create(name="Workflow 1", trigger_type="user_signup")
        AutomationWorkflow.objects.create(name="Workflow 2", trigger_type="event_created")
        
        service = AutomationService()
        workflows = service.get_workflows()
        assert workflows.count() == 2

@pytest.mark.django_db
class TestWorkflowExecutionService:
    def test_execute_workflow(self):
        """Test executing workflow"""
        workflow = AutomationWorkflow.objects.create(
            name="Test",
            trigger_type="user_signup",
            status="active"
        )
        
        service = WorkflowExecutionService()
        result = service.execute_workflow(workflow.id, {'user_id': 123})
        assert result is True

@pytest.mark.django_db
class TestTriggerManagementService:
    def test_create_trigger(self):
        """Test creating trigger"""
        workflow = AutomationWorkflow.objects.create(
            name="Test",
            trigger_type="user_signup",
            status="draft"
        )
        
        service = TriggerManagementService()
        trigger = service.create_trigger(workflow.id, {
            'trigger_type': 'user_signup',
            'conditions': {'user_type': 'new'}
        })
        assert trigger.trigger_type == 'user_signup'
