import pytest
from domain.models import AutomationWorkflow, WorkflowTrigger

@pytest.mark.django_db
class TestAutomationWorkflow:
    def test_create_workflow(self):
        """Test creating automation workflow"""
        workflow = AutomationWorkflow.objects.create(
            name="Welcome Workflow",
            trigger_type="user_signup",
            status="active"
        )
        assert workflow.name == "Welcome Workflow"
        assert workflow.status == "active"

    def test_workflow_status_choices(self):
        """Test workflow status validation"""
        workflow = AutomationWorkflow.objects.create(
            name="Test",
            trigger_type="event_created",
            status="draft"
        )
        assert workflow.status in ['draft', 'active', 'paused', 'completed']

    def test_activate_workflow(self):
        """Test activating workflow"""
        workflow = AutomationWorkflow.objects.create(
            name="Test",
            trigger_type="user_signup",
            status="draft"
        )
        workflow.activate()
        assert workflow.status == "active"

    def test_pause_workflow(self):
        """Test pausing workflow"""
        workflow = AutomationWorkflow.objects.create(
            name="Test",
            trigger_type="user_signup",
            status="active"
        )
        workflow.pause()
        assert workflow.status == "paused"

@pytest.mark.django_db
class TestWorkflowTrigger:
    def test_create_trigger(self):
        """Test creating workflow trigger"""
        workflow = AutomationWorkflow.objects.create(
            name="Test Workflow",
            trigger_type="user_signup",
            status="draft"
        )
        trigger = WorkflowTrigger.objects.create(
            workflow=workflow,
            trigger_type="user_signup",
            conditions={"user_type": "new"}
        )
        assert trigger.trigger_type == "user_signup"
        assert trigger.conditions["user_type"] == "new"

    def test_trigger_validation(self):
        """Test trigger validation"""
        workflow = AutomationWorkflow.objects.create(
            name="Test",
            trigger_type="event_created",
            status="draft"
        )
        trigger = WorkflowTrigger.objects.create(
            workflow=workflow,
            trigger_type="event_created",
            conditions={}
        )
        assert trigger.is_valid()
