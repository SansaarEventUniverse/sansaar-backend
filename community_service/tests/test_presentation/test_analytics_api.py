import pytest
from rest_framework.test import APIClient
from datetime import timedelta
from django.utils import timezone
from domain.models import CommunityAnalytics, EngagementMetrics

@pytest.mark.django_db
class TestAnalyticsAPI:
    def setup_method(self):
        self.client = APIClient()

    def test_get_community_analytics(self):
        """Test getting community analytics"""
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
        
        response = self.client.get('/api/community/analytics/?type=user_growth')
        assert response.status_code == 200
        assert len(response.data) == 1

    def test_get_engagement_report(self):
        """Test getting engagement report"""
        EngagementMetrics.objects.create(
            user_id=1,
            posts_created=10,
            comments_made=20,
            engagement_score=100.0,
            last_active=timezone.now()
        )
        
        response = self.client.get('/api/community/engagement/?days=7')
        assert response.status_code == 200
        assert 'trends' in response.data
        assert 'active_users' in response.data
        assert response.data['period_days'] == 7

    def test_get_insights_dashboard(self):
        """Test getting insights dashboard"""
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
        
        response = self.client.get('/api/community/insights/')
        assert response.status_code == 200
        assert 'top_users' in response.data
        assert 'summary' in response.data
        assert len(response.data['top_users']) == 2
        assert response.data['summary']['total_users'] == 2
