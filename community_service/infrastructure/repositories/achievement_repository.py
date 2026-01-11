from domain.models import UserAchievement, Achievement
from django.db.models import Count, Avg

class AchievementRepository:
    def get_user_stats(self, user_id):
        total = UserAchievement.objects.filter(user_id=user_id).count()
        completed = UserAchievement.objects.filter(user_id=user_id, status='completed').count()
        total_points = sum(
            ua.achievement.points for ua in UserAchievement.objects.filter(
                user_id=user_id, status='completed'
            ).select_related('achievement')
        )
        
        return {
            'total_achievements': total,
            'completed_achievements': completed,
            'total_points': total_points,
            'completion_rate': (completed / total * 100) if total > 0 else 0
        }
    
    def get_leaderboard(self, limit=10):
        from django.db.models import Sum
        leaderboard = UserAchievement.objects.filter(
            status='completed'
        ).values('user_id').annotate(
            total_points=Sum('achievement__points'),
            achievement_count=Count('id')
        ).order_by('-total_points')[:limit]
        
        return list(leaderboard)
