import pytest
from domain.models import Achievement, UserAchievement
from infrastructure.repositories.achievement_repository import AchievementRepository

@pytest.mark.django_db
class TestAchievementRepository:
    def test_get_user_stats(self):
        a1 = Achievement.objects.create(name='A1', description='Test', category='participation', points=10, criteria='Test')
        a2 = Achievement.objects.create(name='A2', description='Test', category='learning', points=20, criteria='Test')
        UserAchievement.objects.create(achievement=a1, user_id=1, status='completed', progress=100)
        UserAchievement.objects.create(achievement=a2, user_id=1, status='in_progress', progress=50)
        
        repo = AchievementRepository()
        stats = repo.get_user_stats(1)
        assert stats['total_achievements'] == 2
        assert stats['completed_achievements'] == 1
        assert stats['total_points'] == 10
        assert stats['completion_rate'] == 50.0
    
    def test_get_leaderboard(self):
        a1 = Achievement.objects.create(name='A1', description='Test', category='participation', points=10, criteria='Test')
        a2 = Achievement.objects.create(name='A2', description='Test', category='learning', points=20, criteria='Test')
        a3 = Achievement.objects.create(name='A3', description='Test', category='leadership', points=50, criteria='Test')
        
        UserAchievement.objects.create(achievement=a1, user_id=1, status='completed', progress=100)
        UserAchievement.objects.create(achievement=a2, user_id=1, status='completed', progress=100)
        UserAchievement.objects.create(achievement=a3, user_id=2, status='completed', progress=100)
        
        repo = AchievementRepository()
        leaderboard = repo.get_leaderboard(limit=5)
        assert len(leaderboard) == 2
        assert leaderboard[0]['user_id'] == 2
        assert leaderboard[0]['total_points'] == 50
