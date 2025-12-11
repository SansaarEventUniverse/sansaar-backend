from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from application.services.dashboard_service import DashboardService
from presentation.serializers.dashboard_serializers import DashboardSerializer, DashboardWidgetSerializer
from domain.models import Dashboard, DashboardWidget


@api_view(['GET'])
def get_dashboard(request, dashboard_id):
    try:
        dashboard = Dashboard.objects.prefetch_related('widgets').get(id=dashboard_id)
        serializer = DashboardSerializer(dashboard)
        return Response(serializer.data)
    except Dashboard.DoesNotExist:
        return Response({'error': 'Dashboard not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def customize_dashboard(request, dashboard_id):
    try:
        service = DashboardService()
        layout = request.data.get('layout', {})
        dashboard = service.update_dashboard_layout(dashboard_id, layout)
        serializer = DashboardSerializer(dashboard)
        return Response(serializer.data)
    except Dashboard.DoesNotExist:
        return Response({'error': 'Dashboard not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_dashboard_widgets(request, dashboard_id):
    try:
        dashboard = Dashboard.objects.get(id=dashboard_id)
        widgets = DashboardWidget.objects.filter(dashboard=dashboard)
        serializer = DashboardWidgetSerializer(widgets, many=True)
        return Response(serializer.data)
    except Dashboard.DoesNotExist:
        return Response({'error': 'Dashboard not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def create_dashboard(request):
    serializer = DashboardSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    service = DashboardService()
    dashboard = service.create_dashboard(
        serializer.validated_data['organizer_id'],
        serializer.validated_data['name'],
        serializer.validated_data.get('layout', {})
    )
    return Response(DashboardSerializer(dashboard).data, status=status.HTTP_201_CREATED)
