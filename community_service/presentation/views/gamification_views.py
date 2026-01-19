from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from application.services.gamification_service import RewardManagementService, LeaderboardService
from infrastructure.repositories.gamification_repository import GamificationRepository
from presentation.serializers.gamification_serializers import UserRewardSerializer

@api_view(['GET'])
def get_user_rewards(request, user_id):
    """Get user rewards"""
    service = RewardManagementService()
    rewards = service.get_user_rewards(user_id)
    total_points = service.get_user_total_points(user_id)
    
    serializer = UserRewardSerializer(rewards, many=True)
    return Response({
        'rewards': serializer.data,
        'total_points': total_points
    })

@api_view(['GET'])
def get_leaderboard(request):
    """Get leaderboard"""
    try:
        limit = int(request.query_params.get('limit', 10))
        if limit <= 0 or limit > 100:
            limit = 10
    except (ValueError, TypeError):
        limit = 10
    
    service = LeaderboardService()
    top_users = service.get_top_users(limit=limit)
    
    return Response({
        'leaderboard': top_users,
        'total_users': len(top_users)
    })

@api_view(['GET'])
def get_gamification_stats(request, user_id):
    """Get user gamification stats"""
    service = RewardManagementService()
    leaderboard_service = LeaderboardService()
    
    rewards = service.get_user_rewards(user_id)
    total_points = service.get_user_total_points(user_id)
    rank = leaderboard_service.get_user_rank(user_id)
    
    user_level = 1
    if rewards.exists():
        user_level = rewards.first().level
    
    return Response({
        'user_id': user_id,
        'total_points': total_points,
        'level': user_level,
        'rank': rank,
        'rewards_count': rewards.count()
    })
