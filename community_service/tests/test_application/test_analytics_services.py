import pytest
from datetime import timedelta
from django.utils import timezone
from domain.models import CommunityAnalytics, EngagementMetrics
from application.services.analytics_service import CommunityAnalyticsService, EngagementTrackingService, InsightsGenerationService

@pytest.mark.django_db
class TestCommunityAnalyticsService:
    def test_create_analytics(self):
        """Test creating analytics"""
        service = CommunityAnalyticsService()
        start = timezone.now()
        end = start + timedelta(days=7)
        analytics = service.create_analytics({
            'metric_type': 'user_growth',
            'metric_value': 100.0,
            'period_start': start,
            'period_end': end
        })
        assert analytics.metric_type == 'user_growth'

    def test_get_analytics_by_type(self):
        """Test getting analytics by type"""
        start = timezone.now()
        end = start + timedelta(days=7)
        CommunityAnalytics.objects.create(
            metric_type='engagement',
            metric_value=100.0,
            period_start=start,
            period_end=end
        )
        CommunityAnalytics.objects.create(
            metric_type='user_growth',
            metric_value=50.0,
            period_start=start,
            period_end=end
        )
        
        service = CommunityAnalyticsService()
        results = service.get_analytics_by_type('engagement')
        assert results.count() == 1

    def test_get_period_analytics(self):
        """Test getting analytics for period"""
        start = timezone.now()
        end = start + timedelta(days=7)
        CommunityAnalytics.objects.create(
            metric_type='engagement',
            metric_value=100.0,
            period_start=start,
            period_end=end
        )
        
        service = CommunityAnalyticsService()
        results = service.get_period_analytics(start, end)
        assert results.count() == 1

@pytest.mark.django_db
class TestEngagementTrackingService:
    def test_track_post_activity(self):
        """Test tracking post activity"""
        service = EngagementTrackingService()
        metrics = service.track_user_engagement(1, 'post')
        assert metrics.posts_created == 1
        assert metrics.engagement_score == 5.0

    def test_track_comment_activity(self):
        """Test tracking comment activity"""
        service = EngagementTrackingService()
        metrics = service.track_user_engagement(1, 'comment')
        assert metrics.comments_made == 1
        assert metrics.engagement_score == 3.0

    def test_track_multiple_activities(self):
        """Test tracking multiple activities"""
        service = EngagementTrackingService()
        service.track_user_engagement(1, 'post')
        service.track_user_engagement(1, 'comment')
        metrics = service.track_user_engagement(1, 'like')
        assert metrics.posts_created == 1
        assert metrics.comments_made == 1
        assert metrics.likes_given == 1
        assert metrics.engagement_score == 9.0  # 5 + 3 + 1

    def test_get_user_engagement(self):
        """Test getting user engagement"""
        EngagementMetrics.objects.create(
            user_id=1,
            posts_created=5,
            engagement_score=25.0
        )
        service = EngagementTrackingService()
        metrics = service.get_user_engagement(1)
        assert metrics.posts_created == 5

@pytest.mark.django_db
class TestInsightsGenerationService:
    def test_generate_top_users(self):
        """Test generating top users"""
        EngagementMetrics.objects.create(user_id=1, engagement_score=100.0)
        EngagementMetrics.objects.create(user_id=2, engagement_score=50.0)
        EngagementMetrics.objects.create(user_id=3, engagement_score=75.0)
        
        service = InsightsGenerationService()
        top_users = service.generate_top_users(limit=2)
        assert len(top_users) == 2
        assert top_users[0].user_id == 1

    def test_generate_engagement_summary(self):
        """Test generating engagement summary"""
        EngagementMetrics.objects.create(
            user_id=1,
            posts_created=10,
            comments_made=20,
            engagement_score=100.0
        )
        EngagementMetrics.objects.create(
            user_id=2,
            posts_created=5,
            comments_made=10,
            engagement_score=50.0
        )
        
        service = InsightsGenerationService()
        summary = service.generate_engagement_summary()
        assert summary['total_users'] == 2
        assert summary['total_posts'] == 15
        assert summary['total_comments'] == 30
        assert summary['average_score'] == 75.0
