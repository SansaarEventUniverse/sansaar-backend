import pytest
from datetime import datetime, timedelta
from django.utils import timezone
from domain.models import CommunityAnalytics, EngagementMetrics

@pytest.mark.django_db
class TestCommunityAnalytics:
    def test_create_analytics(self):
        """Test creating community analytics"""
        start = timezone.now()
        end = start + timedelta(days=7)
        analytics = CommunityAnalytics.objects.create(
            metric_type='user_growth',
            metric_value=150.0,
            period_start=start,
            period_end=end
        )
        assert analytics.metric_type == 'user_growth'
        assert analytics.metric_value == 150.0

    def test_calculate_growth_rate(self):
        """Test calculating growth rate"""
        analytics = CommunityAnalytics.objects.create(
            metric_type='engagement',
            metric_value=120.0,
            period_start=timezone.now(),
            period_end=timezone.now() + timedelta(days=7)
        )
        growth_rate = analytics.calculate_growth_rate(100.0)
        assert growth_rate == 20.0

    def test_calculate_growth_rate_zero_previous(self):
        """Test growth rate with zero previous value"""
        analytics = CommunityAnalytics.objects.create(
            metric_type='engagement',
            metric_value=100.0,
            period_start=timezone.now(),
            period_end=timezone.now() + timedelta(days=7)
        )
        growth_rate = analytics.calculate_growth_rate(0)
        assert growth_rate == 0

@pytest.mark.django_db
class TestEngagementMetrics:
    def test_create_engagement_metrics(self):
        """Test creating engagement metrics"""
        metrics = EngagementMetrics.objects.create(
            user_id=1,
            posts_created=10,
            comments_made=25,
            likes_given=50,
            shares_made=5
        )
        assert metrics.user_id == 1
        assert metrics.posts_created == 10

    def test_calculate_engagement_score(self):
        """Test calculating engagement score"""
        metrics = EngagementMetrics.objects.create(
            user_id=1,
            posts_created=10,
            comments_made=20,
            likes_given=30,
            shares_made=5
        )
        score = metrics.calculate_engagement_score()
        # 10*5 + 20*3 + 30*1 + 5*4 = 50 + 60 + 30 + 20 = 160
        assert score == 160.0
        assert metrics.engagement_score == 160.0

    def test_default_values(self):
        """Test default values for engagement metrics"""
        metrics = EngagementMetrics.objects.create(user_id=1)
        assert metrics.posts_created == 0
        assert metrics.comments_made == 0
        assert metrics.likes_given == 0
        assert metrics.shares_made == 0
        assert metrics.engagement_score == 0.0
