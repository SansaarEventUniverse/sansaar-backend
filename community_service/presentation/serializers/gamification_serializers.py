from rest_framework import serializers
from domain.models import GamificationRule, UserReward

class GamificationRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GamificationRule
        fields = ['id', 'name', 'rule_type', 'points', 'description', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']

class UserRewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReward
        fields = ['id', 'user_id', 'reward_type', 'reward_name', 'points_earned', 'total_points', 'level', 'earned_at']
        read_only_fields = ['id', 'earned_at']
