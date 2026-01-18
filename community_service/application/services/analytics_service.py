from domain.models import CommunityAnalytics, EngagementMetrics
from django.utils import timezone
from datetime import timedelta

class CommunityAnalyticsService:
    def create_analytics(self, data):
        return CommunityAnalytics.objects.create(**data)

    def get_analytics_by_type(self, metric_type):
        return CommunityAnalytics.objects.filter(metric_type=metric_type)

    def get_period_analytics(self, start_date, end_date):
        return CommunityAnalytics.objects.filter(
            period_start__gte=start_date,
            period_end__lte=end_date
        )

class EngagementTrackingService:
    def track_user_engagement(self, user_id, activity_type):
        metrics, created = EngagementMetrics.objects.get_or_create(user_id=user_id)
        
        if activity_type == 'post':
            metrics.posts_created += 1
        elif activity_type == 'comment':
            metrics.comments_made += 1
        elif activity_type == 'like':
            metrics.likes_given += 1
        elif activity_type == 'share':
            metrics.shares_made += 1
        
        metrics.last_active = timezone.now()
        metrics.calculate_engagement_score()
        return metrics

    def get_user_engagement(self, user_id):
        return EngagementMetrics.objects.filter(user_id=user_id).first()

class InsightsGenerationService:
    def generate_top_users(self, limit=10):
        return EngagementMetrics.objects.order_by('-engagement_score')[:limit]

    def generate_engagement_summary(self):
        metrics = EngagementMetrics.objects.all()
        return {
            'total_users': metrics.count(),
            'total_posts': sum(m.posts_created for m in metrics),
            'total_comments': sum(m.comments_made for m in metrics),
            'average_score': sum(m.engagement_score for m in metrics) / metrics.count() if metrics.count() > 0 else 0
        }
