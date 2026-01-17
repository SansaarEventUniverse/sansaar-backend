import pytest
from domain.models import GamificationRule, UserReward

@pytest.mark.django_db
class TestGamificationRule:
    def test_create_rule(self):
        """Test creating gamification rule"""
        rule = GamificationRule.objects.create(
            name="First Post",
            rule_type='post_created',
            points=10,
            description="Earn points for creating your first post"
        )
        assert rule.name == "First Post"
        assert rule.points == 10
        assert rule.is_active is True

    def test_rule_types(self):
        """Test different rule types"""
        rule1 = GamificationRule.objects.create(
            name="Comment Reward",
            rule_type='comment_made',
            points=5
        )
        rule2 = GamificationRule.objects.create(
            name="Like Reward",
            rule_type='like_received',
            points=2
        )
        assert rule1.rule_type == 'comment_made'
        assert rule2.rule_type == 'like_received'

@pytest.mark.django_db
class TestUserReward:
    def test_create_reward(self):
        """Test creating user reward"""
        reward = UserReward.objects.create(
            user_id=1,
            reward_type='points',
            reward_name="Activity Points",
            points_earned=50
        )
        assert reward.user_id == 1
        assert reward.points_earned == 50
        assert reward.level == 1

    def test_add_points(self):
        """Test adding points to user"""
        reward = UserReward.objects.create(
            user_id=1,
            reward_type='points',
            reward_name="Activity Points",
            total_points=50
        )
        reward.add_points(30)
        assert reward.points_earned == 30
        assert reward.total_points == 80
        assert reward.level == 1

    def test_level_calculation(self):
        """Test level calculation based on points"""
        reward = UserReward.objects.create(
            user_id=1,
            reward_type='points',
            reward_name="Activity Points"
        )
        reward.add_points(250)
        assert reward.total_points == 250
        assert reward.level == 3  # 250 // 100 + 1 = 3

    def test_reward_types(self):
        """Test different reward types"""
        badge = UserReward.objects.create(
            user_id=1,
            reward_type='badge',
            reward_name="Top Contributor"
        )
        achievement = UserReward.objects.create(
            user_id=1,
            reward_type='achievement',
            reward_name="100 Posts"
        )
        assert badge.reward_type == 'badge'
        assert achievement.reward_type == 'achievement'
