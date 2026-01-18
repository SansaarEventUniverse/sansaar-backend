from domain.models import GamificationRule, UserReward

class GamificationService:
    def create_rule(self, data):
        return GamificationRule.objects.create(**data)

    def get_active_rules(self):
        return GamificationRule.objects.filter(is_active=True)

    def get_rule_by_type(self, rule_type):
        return GamificationRule.objects.filter(rule_type=rule_type, is_active=True).first()

class RewardManagementService:
    def award_points(self, user_id, rule_type):
        rule = GamificationRule.objects.filter(rule_type=rule_type, is_active=True).first()
        if not rule:
            return None
        
        reward, created = UserReward.objects.get_or_create(
            user_id=user_id,
            reward_type='points',
            defaults={'reward_name': 'Activity Points'}
        )
        reward.add_points(rule.points)
        return reward

    def get_user_rewards(self, user_id):
        return UserReward.objects.filter(user_id=user_id)

    def get_user_total_points(self, user_id):
        rewards = UserReward.objects.filter(user_id=user_id, reward_type='points')
        return sum(r.total_points for r in rewards)

class LeaderboardService:
    def get_top_users(self, limit=10):
        rewards = UserReward.objects.filter(reward_type='points').order_by('-total_points')[:limit]
        return [{'user_id': r.user_id, 'total_points': r.total_points, 'level': r.level} for r in rewards]

    def get_user_rank(self, user_id):
        user_reward = UserReward.objects.filter(user_id=user_id, reward_type='points').first()
        if not user_reward:
            return None
        
        higher_ranks = UserReward.objects.filter(
            reward_type='points',
            total_points__gt=user_reward.total_points
        ).count()
        return higher_ranks + 1
