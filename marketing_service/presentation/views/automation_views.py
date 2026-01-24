from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from application.services.automation_service import AutomationService, WorkflowExecutionService
from presentation.serializers.automation_serializers import AutomationWorkflowSerializer, ExecuteWorkflowSerializer

@api_view(['GET', 'POST'])
def workflow_list_create(request):
    service = AutomationService()
    
    if request.method == 'GET':
        workflows = service.get_workflows()
        serializer = AutomationWorkflowSerializer(workflows, many=True)
        return Response(serializer.data)
    
    serializer = AutomationWorkflowSerializer(data=request.data)
    if serializer.is_valid():
        workflow = service.create_workflow(serializer.validated_data)
        return Response(AutomationWorkflowSerializer(workflow).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def execute_workflow(request, workflow_id):
    serializer = ExecuteWorkflowSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    service = WorkflowExecutionService()
    service.execute_workflow(workflow_id, serializer.validated_data['context'])
    
    return Response({'status': 'Workflow executed'})
