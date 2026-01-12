from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from application.services.content_service import ContentSharingService, CollaborationService, ContentModerationService
from infrastructure.repositories.content_repository import ContentRepository
from presentation.serializers.content_serializers import SharedContentSerializer, ContentCollaborationSerializer

@api_view(['POST'])
def share_content(request):
    serializer = SharedContentSerializer(data=request.data)
    if serializer.is_valid():
        service = ContentSharingService()
        content = service.create_content(serializer.validated_data)
        response_serializer = SharedContentSerializer(content)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_shared_content(request):
    service = ContentSharingService()
    content = service.get_published_content()
    serializer = SharedContentSerializer(content, many=True)
    return Response({'results': serializer.data})

@api_view(['POST'])
def collaborate(request, content_id):
    user_id = request.data.get('user_id')
    role = request.data.get('role', 'viewer')
    
    if not user_id:
        return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    service = CollaborationService()
    collab = service.add_collaborator(content_id, int(user_id), role)
    serializer = ContentCollaborationSerializer(collab)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_collaborators(request, content_id):
    service = CollaborationService()
    collabs = service.get_collaborators(content_id)
    serializer = ContentCollaborationSerializer(collabs, many=True)
    return Response({'results': serializer.data})
