from rest_framework import serializers
from domain.models import AutomationWorkflow, WorkflowTrigger

class AutomationWorkflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutomationWorkflow
        fields = '__all__'

class WorkflowTriggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowTrigger
        fields = '__all__'

class ExecuteWorkflowSerializer(serializers.Serializer):
    context = serializers.JSONField()
