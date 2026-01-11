import pytest
from rest_framework.test import APIClient
from domain.models import Achievement, UserAchievement

@pytest.mark.django_db
class TestAchievementAPI:
    def test_create_achievement(self):
        client = APIClient()
        data = {
            'name': 'First Post',
            'description': 'Create your first forum post',
            'category': 'participation',
            'points': 10,
            'criteria': 'Create 1 forum post'
        }
        response = client.post('/api/community/achievements/create/', data, format='json')
        assert response.status_code == 201
        assert response.data['name'] == 'First Post'
    
    def test_get_achievements(self):
        Achievement.objects.create(name='A1', description='Test', category='participation', points=10, criteria='Test')
        Achievement.objects.create(name='A2', description='Test', category='learning', points=20, criteria='Test')
        client = APIClient()
        response = client.get('/api/community/achievements/')
        assert response.status_code == 200
        assert len(response.data['results']) == 2
    
    def test_get_achievements_by_category(self):
        Achievement.objects.create(name='A1', description='Test', category='participation', points=10, criteria='Test')
        Achievement.objects.create(name='A2', description='Test', category='participation', points=15, criteria='Test')
        Achievement.objects.create(name='A3', description='Test', category='leadership', points=50, criteria='Test')
        client = APIClient()
        response = client.get('/api/community/achievements/?category=participation')
        assert response.status_code == 200
        assert len(response.data['results']) == 2
    
    def test_get_user_achievements(self):
        achievement = Achievement.objects.create(name='Test', description='Test', category='contribution', points=20, criteria='Test')
        UserAchievement.objects.create(achievement=achievement, user_id=1, progress=50)
        client = APIClient()
        response = client.get('/api/community/users/1/achievements/')
        assert response.status_code == 200
        assert len(response.data['results']) == 1
    
    def test_get_user_progress(self):
        a1 = Achievement.objects.create(name='A1', description='Test', category='participation', points=10, criteria='Test')
        a2 = Achievement.objects.create(name='A2', description='Test', category='learning', points=20, criteria='Test')
        UserAchievement.objects.create(achievement=a1, user_id=1, status='completed', progress=100)
        UserAchievement.objects.create(achievement=a2, user_id=1, status='in_progress', progress=50)
        client = APIClient()
        response = client.get('/api/community/users/1/progress/')
        assert response.status_code == 200
        assert response.data['total_achievements'] == 2
        assert response.data['completed_achievements'] == 1
