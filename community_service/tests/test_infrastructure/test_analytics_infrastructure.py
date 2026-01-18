import pytest
from datetime import timedelta
from django.utils import timezone
from domain.models import CommunityAnalytics, EngagementMetrics
from infrastructure.repositories.analytics_repository import AnalyticsRepository

@pytest.mark.django_db
class TestAnalyticsRepository:
    def test_get_engagement_trends(self):
        """Test getting engagement trends"""
        EngagementMetrics.objects.create(
            user_id=1,
            posts_created=10,
            comments_made=20,
            engagement_score=100.0,
            last_active=timezone.now()
        )
        EngagementMetrics.objects.create(
            user_id=2,
            posts_created=5,
            comments_made=10,
            engagement_score=50.0,
            last_active=timezone.now()
        )
        
        repo = AnalyticsRepository()
        trends = repo.get_engagement_trends(days=7)
        
        assert trends['avg_score'] == 75.0
        assert trends['total_posts'] == 15
        assert trends['total_comments'] == 30
        assert trends['active_users'] == 2

    def test_get_growth_metrics(self):
        """Test getting growth metrics"""
        start = timezone.now()
        end = start + timedelta(days=7)
        CommunityAnalytics.objects.create(
            metric_type='user_growth',
            metric_value=100.0,
            period_start=start,
            period_end=end
        )
        CommunityAnalytics.objects.create(
            metric_type='engagement',
            metric_value=50.0,
            period_start=start,
            period_end=end
        )
        
        repo = AnalyticsRepository()
        metrics = repo.get_growth_metrics('user_growth')
        assert metrics.count() == 1

    def test_get_active_users_count(self):
        """Test getting active users count"""
        EngagementMetrics.objects.create(
            user_id=1,
            last_active=timezone.now()
        )
        EngagementMetrics.objects.create(
            user_id=2,
            last_active=timezone.now() - timedelta(days=40)
        )
        
        repo = AnalyticsRepository()
        count = repo.get_active_users_count(days=30)
        assert count == 1
