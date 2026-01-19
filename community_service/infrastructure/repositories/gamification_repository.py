from domain.models import GamificationRule, UserReward
from django.db.models import Sum, Count, Avg

class GamificationRepository:
    def get_reward_statistics(self):
        return {
            'total_rewards': UserReward.objects.count(),
            'total_points_distributed': UserReward.objects.aggregate(Sum('total_points'))['total_points__sum'] or 0,
            'average_level': UserReward.objects.aggregate(Avg('level'))['level__avg'] or 0
        }

    def get_rule_usage_stats(self, rule_id):
        rule = GamificationRule.objects.get(id=rule_id)
        return {
            'rule_name': rule.name,
            'points_per_action': rule.points,
            'is_active': rule.is_active
        }

    def get_users_by_level(self, level):
        return UserReward.objects.filter(level=level, reward_type='points')
