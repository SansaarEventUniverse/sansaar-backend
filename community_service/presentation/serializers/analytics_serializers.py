from rest_framework import serializers
from domain.models import CommunityAnalytics, EngagementMetrics

class CommunityAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityAnalytics
        fields = ['id', 'metric_type', 'metric_value', 'period_start', 'period_end', 'metadata', 'created_at']
        read_only_fields = ['id', 'created_at']

class EngagementMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngagementMetrics
        fields = ['id', 'user_id', 'posts_created', 'comments_made', 'likes_given', 'shares_made', 'engagement_score', 'last_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'engagement_score', 'created_at', 'updated_at']
