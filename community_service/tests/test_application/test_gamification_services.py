import pytest
from domain.models import GamificationRule, UserReward
from application.services.gamification_service import GamificationService, RewardManagementService, LeaderboardService

@pytest.mark.django_db
class TestGamificationService:
    def test_create_rule(self):
        """Test creating gamification rule"""
        service = GamificationService()
        rule = service.create_rule({
            'name': 'Post Reward',
            'rule_type': 'post_created',
            'points': 10
        })
        assert rule.name == 'Post Reward'

    def test_get_active_rules(self):
        """Test getting active rules"""
        GamificationRule.objects.create(name="Rule 1", rule_type='post_created', points=10, is_active=True)
        GamificationRule.objects.create(name="Rule 2", rule_type='comment_made', points=5, is_active=True)
        GamificationRule.objects.create(name="Rule 3", rule_type='like_received', points=2, is_active=False)
        
        service = GamificationService()
        rules = service.get_active_rules()
        assert rules.count() == 2

    def test_get_rule_by_type(self):
        """Test getting rule by type"""
        GamificationRule.objects.create(name="Post Rule", rule_type='post_created', points=10)
        
        service = GamificationService()
        rule = service.get_rule_by_type('post_created')
        assert rule.name == "Post Rule"

@pytest.mark.django_db
class TestRewardManagementService:
    def test_award_points(self):
        """Test awarding points to user"""
        GamificationRule.objects.create(name="Post Rule", rule_type='post_created', points=10)
        
        service = RewardManagementService()
        reward = service.award_points(1, 'post_created')
        assert reward.points_earned == 10
        assert reward.total_points == 10

    def test_award_points_multiple_times(self):
        """Test awarding points multiple times"""
        GamificationRule.objects.create(name="Post Rule", rule_type='post_created', points=10)
        
        service = RewardManagementService()
        service.award_points(1, 'post_created')
        reward = service.award_points(1, 'post_created')
        assert reward.total_points == 20

    def test_get_user_rewards(self):
        """Test getting user rewards"""
        UserReward.objects.create(user_id=1, reward_type='points', reward_name='Points', total_points=50)
        UserReward.objects.create(user_id=1, reward_type='badge', reward_name='Badge')
        
        service = RewardManagementService()
        rewards = service.get_user_rewards(1)
        assert rewards.count() == 2

    def test_get_user_total_points(self):
        """Test getting user total points"""
        UserReward.objects.create(user_id=1, reward_type='points', reward_name='Points', total_points=50)
        
        service = RewardManagementService()
        total = service.get_user_total_points(1)
        assert total == 50

@pytest.mark.django_db
class TestLeaderboardService:
    def test_get_top_users(self):
        """Test getting top users"""
        UserReward.objects.create(user_id=1, reward_type='points', reward_name='Points', total_points=100, level=2)
        UserReward.objects.create(user_id=2, reward_type='points', reward_name='Points', total_points=50, level=1)
        UserReward.objects.create(user_id=3, reward_type='points', reward_name='Points', total_points=75, level=1)
        
        service = LeaderboardService()
        top_users = service.get_top_users(limit=2)
        assert len(top_users) == 2
        assert top_users[0]['user_id'] == 1
        assert top_users[0]['total_points'] == 100

    def test_get_user_rank(self):
        """Test getting user rank"""
        UserReward.objects.create(user_id=1, reward_type='points', reward_name='Points', total_points=100)
        UserReward.objects.create(user_id=2, reward_type='points', reward_name='Points', total_points=50)
        UserReward.objects.create(user_id=3, reward_type='points', reward_name='Points', total_points=75)
        
        service = LeaderboardService()
        rank = service.get_user_rank(3)
        assert rank == 2  # User 3 is ranked 2nd (after user 1)
