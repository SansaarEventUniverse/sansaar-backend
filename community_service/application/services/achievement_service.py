from domain.models import Achievement, UserAchievement

class AchievementService:
    def create_achievement(self, data):
        return Achievement.objects.create(**data)
    
    def get_active_achievements(self):
        return Achievement.objects.filter(is_active=True)
    
    def get_achievements_by_category(self, category):
        return Achievement.objects.filter(category=category, is_active=True)

class ProgressTrackingService:
    def track_progress(self, user_id, achievement_id, progress):
        user_achievement, created = UserAchievement.objects.get_or_create(
            user_id=user_id,
            achievement_id=achievement_id
        )
        user_achievement.update_progress(progress)
        return user_achievement
    
    def get_user_progress(self, user_id):
        return UserAchievement.objects.filter(user_id=user_id)
    
    def get_completed_achievements(self, user_id):
        return UserAchievement.objects.filter(user_id=user_id, status='completed')

class BadgeManagementService:
    def award_badge(self, user_id, achievement_id):
        user_achievement, created = UserAchievement.objects.get_or_create(
            user_id=user_id,
            achievement_id=achievement_id
        )
        user_achievement.complete()
        return user_achievement
    
    def get_user_badges(self, user_id):
        return UserAchievement.objects.filter(user_id=user_id, status='completed')
