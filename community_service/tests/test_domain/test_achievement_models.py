import pytest
from domain.models import Achievement, UserAchievement

@pytest.mark.django_db
class TestAchievement:
    def test_create_achievement(self):
        achievement = Achievement.objects.create(
            name='First Post',
            description='Create your first forum post',
            category='participation',
            points=10,
            criteria='Create 1 forum post'
        )
        assert achievement.name == 'First Post'
        assert achievement.is_active is True
    
    def test_achievement_categories(self):
        a1 = Achievement.objects.create(name='A1', description='Test', category='participation', points=10, criteria='Test')
        a2 = Achievement.objects.create(name='A2', description='Test', category='leadership', points=50, criteria='Test')
        assert a1.category == 'participation'
        assert a2.category == 'leadership'

@pytest.mark.django_db
class TestUserAchievement:
    def test_create_user_achievement(self):
        achievement = Achievement.objects.create(name='Test', description='Test', category='learning', points=20, criteria='Test')
        user_achievement = UserAchievement.objects.create(achievement=achievement, user_id=1)
        assert user_achievement.status == 'in_progress'
        assert user_achievement.progress == 0
    
    def test_update_progress(self):
        achievement = Achievement.objects.create(name='Test', description='Test', category='contribution', points=30, criteria='Test')
        user_achievement = UserAchievement.objects.create(achievement=achievement, user_id=1)
        user_achievement.update_progress(50)
        assert user_achievement.progress == 50
        assert user_achievement.status == 'in_progress'
    
    def test_complete_achievement(self):
        achievement = Achievement.objects.create(name='Test', description='Test', category='participation', points=10, criteria='Test')
        user_achievement = UserAchievement.objects.create(achievement=achievement, user_id=1)
        user_achievement.complete()
        assert user_achievement.is_completed() is True
        assert user_achievement.progress == 100
        assert user_achievement.completed_at is not None
    
    def test_auto_complete_on_100_progress(self):
        achievement = Achievement.objects.create(name='Test', description='Test', category='learning', points=15, criteria='Test')
        user_achievement = UserAchievement.objects.create(achievement=achievement, user_id=1)
        user_achievement.update_progress(100)
        assert user_achievement.is_completed() is True
    
    def test_progress_capped_at_100(self):
        achievement = Achievement.objects.create(name='Test', description='Test', category='contribution', points=25, criteria='Test')
        user_achievement = UserAchievement.objects.create(achievement=achievement, user_id=1)
        user_achievement.update_progress(150)
        assert user_achievement.progress == 100
