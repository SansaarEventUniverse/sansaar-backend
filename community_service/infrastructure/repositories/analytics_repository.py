from domain.models import CommunityAnalytics, EngagementMetrics
from django.db.models import Avg, Sum, Count
from django.utils import timezone
from datetime import timedelta

class AnalyticsRepository:
    def get_engagement_trends(self, days=7):
        start_date = timezone.now() - timedelta(days=days)
        return EngagementMetrics.objects.filter(
            last_active__gte=start_date
        ).aggregate(
            avg_score=Avg('engagement_score'),
            total_posts=Sum('posts_created'),
            total_comments=Sum('comments_made'),
            active_users=Count('id')
        )

    def get_growth_metrics(self, metric_type):
        return CommunityAnalytics.objects.filter(
            metric_type=metric_type
        ).order_by('-period_end')[:10]

    def get_active_users_count(self, days=30):
        start_date = timezone.now() - timedelta(days=days)
        return EngagementMetrics.objects.filter(
            last_active__gte=start_date
        ).count()
