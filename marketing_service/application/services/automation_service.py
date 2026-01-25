from domain.models import AutomationWorkflow, WorkflowTrigger

class AutomationService:
    def create_workflow(self, data):
        return AutomationWorkflow.objects.create(**data)

    def get_workflows(self):
        return AutomationWorkflow.objects.all()

    def get_workflow(self, workflow_id):
        return AutomationWorkflow.objects.get(id=workflow_id)

class WorkflowExecutionService:
    def execute_workflow(self, workflow_id, context):
        workflow = AutomationWorkflow.objects.get(id=workflow_id)
        if workflow.status == 'active':
            return True
        return False

class TriggerManagementService:
    def create_trigger(self, workflow_id, data):
        workflow = AutomationWorkflow.objects.get(id=workflow_id)
        return WorkflowTrigger.objects.create(workflow=workflow, **data)

    def get_triggers(self, workflow_id):
        return WorkflowTrigger.objects.filter(workflow_id=workflow_id)
