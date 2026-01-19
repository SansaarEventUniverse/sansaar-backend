import pytest
from rest_framework.test import APIClient
from domain.models import GamificationRule, UserReward

@pytest.mark.django_db
class TestGamificationAPI:
    def setup_method(self):
        self.client = APIClient()

    def test_get_user_rewards_success(self):
        """Test getting user rewards - success case"""
        UserReward.objects.create(
            user_id=1,
            reward_type='points',
            reward_name='Activity Points',
            total_points=100,
            level=2
        )
        
        response = self.client.get('/api/community/users/1/rewards/')
        assert response.status_code == 200
        assert 'rewards' in response.data
        assert 'total_points' in response.data
        assert response.data['total_points'] == 100
        assert len(response.data['rewards']) == 1
        assert response.data['rewards'][0]['user_id'] == 1
        assert response.data['rewards'][0]['reward_type'] == 'points'

    def test_get_user_rewards_no_rewards(self):
        """Test getting user rewards when user has no rewards"""
        response = self.client.get('/api/community/users/999/rewards/')
        assert response.status_code == 200
        assert response.data['rewards'] == []
        assert response.data['total_points'] == 0

    def test_get_user_rewards_multiple_rewards(self):
        """Test getting multiple rewards for a user"""
        UserReward.objects.create(user_id=1, reward_type='points', reward_name='Points', total_points=50)
        UserReward.objects.create(user_id=1, reward_type='badge', reward_name='Top Contributor', total_points=0)
        UserReward.objects.create(user_id=1, reward_type='achievement', reward_name='100 Posts', total_points=0)
        
        response = self.client.get('/api/community/users/1/rewards/')
        assert response.status_code == 200
        assert len(response.data['rewards']) == 3
        assert response.data['total_points'] == 50

    def test_get_leaderboard_default(self):
        """Test getting leaderboard with default limit"""
        UserReward.objects.create(user_id=1, reward_type='points', reward_name='Points', total_points=100, level=2)
        UserReward.objects.create(user_id=2, reward_type='points', reward_name='Points', total_points=50, level=1)
        UserReward.objects.create(user_id=3, reward_type='points', reward_name='Points', total_points=75, level=1)
        
        response = self.client.get('/api/community/leaderboard/')
        assert response.status_code == 200
        assert 'leaderboard' in response.data
        assert 'total_users' in response.data
        assert len(response.data['leaderboard']) == 3
        assert response.data['leaderboard'][0]['user_id'] == 1
        assert response.data['leaderboard'][0]['total_points'] == 100
        assert response.data['total_users'] == 3

    def test_get_leaderboard_with_limit(self):
        """Test getting leaderboard with custom limit"""
        UserReward.objects.create(user_id=1, reward_type='points', reward_name='Points', total_points=100)
        UserReward.objects.create(user_id=2, reward_type='points', reward_name='Points', total_points=50)
        UserReward.objects.create(user_id=3, reward_type='points', reward_name='Points', total_points=75)
        
        response = self.client.get('/api/community/leaderboard/?limit=2')
        assert response.status_code == 200
        assert len(response.data['leaderboard']) == 2
        assert response.data['total_users'] == 2

    def test_get_leaderboard_invalid_limit(self):
        """Test leaderboard with invalid limit - should use default"""
        UserReward.objects.create(user_id=1, reward_type='points', reward_name='Points', total_points=100)
        
        response = self.client.get('/api/community/leaderboard/?limit=invalid')
        assert response.status_code == 200
        assert 'leaderboard' in response.data

    def test_get_leaderboard_negative_limit(self):
        """Test leaderboard with negative limit - should use default"""
        UserReward.objects.create(user_id=1, reward_type='points', reward_name='Points', total_points=100)
        
        response = self.client.get('/api/community/leaderboard/?limit=-5')
        assert response.status_code == 200
        assert 'leaderboard' in response.data

    def test_get_leaderboard_empty(self):
        """Test getting leaderboard when no users have rewards"""
        response = self.client.get('/api/community/leaderboard/')
        assert response.status_code == 200
        assert response.data['leaderboard'] == []
        assert response.data['total_users'] == 0

    def test_get_gamification_stats_success(self):
        """Test getting user gamification stats - success case"""
        UserReward.objects.create(
            user_id=1,
            reward_type='points',
            reward_name='Points',
            total_points=100,
            level=2
        )
        UserReward.objects.create(
            user_id=2,
            reward_type='points',
            reward_name='Points',
            total_points=150,
            level=2
        )
        
        response = self.client.get('/api/community/users/1/gamification/')
        assert response.status_code == 200
        assert response.data['user_id'] == 1
        assert response.data['total_points'] == 100
        assert response.data['level'] == 2
        assert response.data['rank'] == 2
        assert response.data['rewards_count'] == 1

    def test_get_gamification_stats_no_rewards(self):
        """Test getting gamification stats for user with no rewards"""
        response = self.client.get('/api/community/users/999/gamification/')
        assert response.status_code == 200
        assert response.data['user_id'] == 999
        assert response.data['total_points'] == 0
        assert response.data['level'] == 1
        assert response.data['rank'] is None
        assert response.data['rewards_count'] == 0

    def test_get_gamification_stats_top_user(self):
        """Test getting stats for top ranked user"""
        UserReward.objects.create(user_id=1, reward_type='points', reward_name='Points', total_points=200, level=3)
        UserReward.objects.create(user_id=2, reward_type='points', reward_name='Points', total_points=100, level=2)
        
        response = self.client.get('/api/community/users/1/gamification/')
        assert response.status_code == 200
        assert response.data['rank'] == 1
        assert response.data['level'] == 3
