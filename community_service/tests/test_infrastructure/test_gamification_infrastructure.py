import pytest
from domain.models import GamificationRule, UserReward
from infrastructure.repositories.gamification_repository import GamificationRepository

@pytest.mark.django_db
class TestGamificationRepository:
    def test_get_reward_statistics(self):
        """Test getting reward statistics"""
        UserReward.objects.create(user_id=1, reward_type='points', reward_name='Points', total_points=100, level=2)
        UserReward.objects.create(user_id=2, reward_type='points', reward_name='Points', total_points=50, level=1)
        
        repo = GamificationRepository()
        stats = repo.get_reward_statistics()
        
        assert stats['total_rewards'] == 2
        assert stats['total_points_distributed'] == 150
        assert stats['average_level'] == 1.5

    def test_get_rule_usage_stats(self):
        """Test getting rule usage statistics"""
        rule = GamificationRule.objects.create(
            name="Post Rule",
            rule_type='post_created',
            points=10,
            is_active=True
        )
        
        repo = GamificationRepository()
        stats = repo.get_rule_usage_stats(rule.id)
        
        assert stats['rule_name'] == "Post Rule"
        assert stats['points_per_action'] == 10
        assert stats['is_active'] is True

    def test_get_users_by_level(self):
        """Test getting users by level"""
        UserReward.objects.create(user_id=1, reward_type='points', reward_name='Points', level=2)
        UserReward.objects.create(user_id=2, reward_type='points', reward_name='Points', level=2)
        UserReward.objects.create(user_id=3, reward_type='points', reward_name='Points', level=1)
        
        repo = GamificationRepository()
        users = repo.get_users_by_level(2)
        assert users.count() == 2
