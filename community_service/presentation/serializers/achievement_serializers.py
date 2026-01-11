from rest_framework import serializers
from domain.models import Achievement, UserAchievement

class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ['id', 'name', 'description', 'category', 'points', 'badge_icon', 'criteria', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']

class UserAchievementSerializer(serializers.ModelSerializer):
    achievement = AchievementSerializer(read_only=True)
    
    class Meta:
        model = UserAchievement
        fields = ['id', 'achievement', 'user_id', 'status', 'progress', 'completed_at', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
