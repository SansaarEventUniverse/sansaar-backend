import pytest
from domain.models import Achievement, UserAchievement
from application.services.achievement_service import AchievementService, ProgressTrackingService, BadgeManagementService

@pytest.mark.django_db
class TestAchievementService:
    def test_create_achievement(self):
        service = AchievementService()
        achievement = service.create_achievement({
            'name': 'First Post',
            'description': 'Create first post',
            'category': 'participation',
            'points': 10,
            'criteria': 'Create 1 post'
        })
        assert achievement.name == 'First Post'
    
    def test_get_active_achievements(self):
        Achievement.objects.create(name='A1', description='Test', category='participation', points=10, criteria='Test', is_active=True)
        Achievement.objects.create(name='A2', description='Test', category='learning', points=20, criteria='Test', is_active=False)
        service = AchievementService()
        achievements = service.get_active_achievements()
        assert achievements.count() == 1
    
    def test_get_achievements_by_category(self):
        Achievement.objects.create(name='A1', description='Test', category='participation', points=10, criteria='Test')
        Achievement.objects.create(name='A2', description='Test', category='participation', points=15, criteria='Test')
        Achievement.objects.create(name='A3', description='Test', category='leadership', points=50, criteria='Test')
        service = AchievementService()
        achievements = service.get_achievements_by_category('participation')
        assert achievements.count() == 2

@pytest.mark.django_db
class TestProgressTrackingService:
    def test_track_progress(self):
        achievement = Achievement.objects.create(name='Test', description='Test', category='contribution', points=20, criteria='Test')
        service = ProgressTrackingService()
        user_achievement = service.track_progress(1, achievement.id, 50)
        assert user_achievement.progress == 50
    
    def test_get_user_progress(self):
        a1 = Achievement.objects.create(name='A1', description='Test', category='participation', points=10, criteria='Test')
        a2 = Achievement.objects.create(name='A2', description='Test', category='learning', points=20, criteria='Test')
        UserAchievement.objects.create(achievement=a1, user_id=1, progress=30)
        UserAchievement.objects.create(achievement=a2, user_id=1, progress=70)
        service = ProgressTrackingService()
        progress = service.get_user_progress(1)
        assert progress.count() == 2
    
    def test_get_completed_achievements(self):
        a1 = Achievement.objects.create(name='A1', description='Test', category='participation', points=10, criteria='Test')
        a2 = Achievement.objects.create(name='A2', description='Test', category='learning', points=20, criteria='Test')
        UserAchievement.objects.create(achievement=a1, user_id=1, status='completed', progress=100)
        UserAchievement.objects.create(achievement=a2, user_id=1, status='in_progress', progress=50)
        service = ProgressTrackingService()
        completed = service.get_completed_achievements(1)
        assert completed.count() == 1

@pytest.mark.django_db
class TestBadgeManagementService:
    def test_award_badge(self):
        achievement = Achievement.objects.create(name='Test', description='Test', category='leadership', points=50, criteria='Test')
        service = BadgeManagementService()
        user_achievement = service.award_badge(1, achievement.id)
        assert user_achievement.is_completed()
    
    def test_get_user_badges(self):
        a1 = Achievement.objects.create(name='A1', description='Test', category='participation', points=10, criteria='Test')
        a2 = Achievement.objects.create(name='A2', description='Test', category='learning', points=20, criteria='Test')
        UserAchievement.objects.create(achievement=a1, user_id=1, status='completed', progress=100)
        UserAchievement.objects.create(achievement=a2, user_id=1, status='in_progress', progress=50)
        service = BadgeManagementService()
        badges = service.get_user_badges(1)
        assert badges.count() == 1
