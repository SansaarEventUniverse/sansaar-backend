from rest_framework import serializers
from domain.models import UserAnalytics, UserActivity


class UserAnalyticsSerializer(serializers.ModelSerializer):
    engagement_score = serializers.SerializerMethodField()

    class Meta:
        model = UserAnalytics
        fields = ['user_id', 'total_events_attended', 'total_tickets_purchased', 'engagement_score', 'created_at', 'updated_at']

    def get_engagement_score(self, obj):
        return obj.calculate_engagement_score()


class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity
        fields = ['user_id', 'activity_type', 'event_id', 'created_at']
