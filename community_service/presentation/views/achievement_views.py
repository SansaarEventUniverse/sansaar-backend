from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from application.services.achievement_service import AchievementService, ProgressTrackingService, BadgeManagementService
from infrastructure.repositories.achievement_repository import AchievementRepository
from presentation.serializers.achievement_serializers import AchievementSerializer, UserAchievementSerializer

@api_view(['POST'])
def create_achievement(request):
    serializer = AchievementSerializer(data=request.data)
    if serializer.is_valid():
        service = AchievementService()
        achievement = service.create_achievement(serializer.validated_data)
        response_serializer = AchievementSerializer(achievement)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_achievements(request):
    category = request.query_params.get('category')
    service = AchievementService()
    
    if category:
        achievements = service.get_achievements_by_category(category)
    else:
        achievements = service.get_active_achievements()
    
    serializer = AchievementSerializer(achievements, many=True)
    return Response({'results': serializer.data})

@api_view(['GET'])
def get_user_achievements(request, user_id):
    service = ProgressTrackingService()
    progress = service.get_user_progress(user_id)
    serializer = UserAchievementSerializer(progress, many=True)
    return Response({'results': serializer.data})

@api_view(['GET'])
def get_user_progress(request, user_id):
    repo = AchievementRepository()
    stats = repo.get_user_stats(user_id)
    return Response(stats)
