from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from application.services.social_media_service import SocialMediaService, ContentSchedulingService
from presentation.serializers.social_media_serializers import SocialMediaPostSerializer, SchedulePostSerializer

@api_view(['GET', 'POST'])
def social_media_post(request):
    service = SocialMediaService()
    
    if request.method == 'GET':
        posts = service.get_posts()
        serializer = SocialMediaPostSerializer(posts, many=True)
        return Response(serializer.data)
    
    serializer = SocialMediaPostSerializer(data=request.data)
    if serializer.is_valid():
        post = service.create_post(serializer.validated_data)
        return Response(SocialMediaPostSerializer(post).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def schedule_post(request):
    serializer = SchedulePostSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    service = ContentSchedulingService()
    service.schedule_post(
        serializer.validated_data['post_id'],
        serializer.validated_data['scheduled_at']
    )
    
    return Response({'status': 'Post scheduled'})
