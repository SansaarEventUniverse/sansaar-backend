from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from application.collaboration_service import EventCollaborationService, TaskManagementService, TeamCoordinationService
from infrastructure.repositories.collaboration_repository import CollaborationRepository
from presentation.serializers.collaboration_serializers import EventCollaborationSerializer, CollaborationTaskSerializer

@api_view(['POST'])
def create_collaboration(request, event_id):
    """Create event collaboration"""
    data = request.data.copy()
    data['event_id'] = event_id
    
    service = EventCollaborationService()
    collab = service.create_collaboration(data)
    serializer = EventCollaborationSerializer(collab)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_collaboration_tasks(request, collaboration_id):
    """Get collaboration tasks"""
    service = TaskManagementService()
    tasks = service.get_tasks(collaboration_id)
    serializer = CollaborationTaskSerializer(tasks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_team_coordination(request, collaboration_id):
    """Get team coordination info"""
    repo = CollaborationRepository()
    stats = repo.get_collaboration_stats(collaboration_id)
    
    service = TeamCoordinationService()
    members = service.get_team_members(collaboration_id)
    
    return Response({
        'stats': stats,
        'team_members': members
    })
