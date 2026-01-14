from rest_framework import serializers
from domain.models import ModerationRule, ModerationAction

class ModerationRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModerationRule
        fields = ['id', 'name', 'rule_type', 'pattern', 'severity', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']

class ModerationActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModerationAction
        fields = ['id', 'rule', 'action_type', 'target_type', 'target_id', 'moderator_id', 'reason', 'status', 'created_at']
        read_only_fields = ['id', 'created_at']
