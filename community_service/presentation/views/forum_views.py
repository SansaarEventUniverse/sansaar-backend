from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from domain.models import Forum, ForumPost
from presentation.serializers.forum_serializers import ForumSerializer, ForumPostSerializer
from application.services.forum_service import ForumService
from application.services.post_management_service import PostManagementService

@api_view(['POST'])
def create_forum(request):
    serializer = ForumSerializer(data=request.data)
    if serializer.is_valid():
        service = ForumService()
        forum = service.create(serializer.validated_data)
        response_serializer = ForumSerializer(forum)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_forums(request):
    forums = Forum.objects.filter(is_active=True)
    serializer = ForumSerializer(forums, many=True)
    return Response({'results': serializer.data})

@api_view(['POST'])
def create_post(request, forum_id):
    data = request.data.copy()
    data['forum'] = forum_id
    
    serializer = ForumPostSerializer(data=data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    service = PostManagementService()
    validated_data = serializer.validated_data.copy()
    validated_data['forum_id'] = validated_data.pop('forum').id
    post = service.create(validated_data)
    response_serializer = ForumPostSerializer(post)
    return Response(response_serializer.data, status=status.HTTP_201_CREATED)
