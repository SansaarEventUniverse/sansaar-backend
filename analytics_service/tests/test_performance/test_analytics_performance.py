import pytest
import time
from django.utils import timezone
from domain.models import AnalyticsEvent, EventMetrics, UserAnalytics, UserActivity
from infrastructure.pipeline.analytics_pipeline import AnalyticsPipeline


@pytest.mark.django_db
class TestAnalyticsPerformance:
    def test_bulk_event_processing(self):
        """Test processing multiple events efficiently"""
        start_time = time.time()
        
        # Create 100 events
        events = [
            AnalyticsEvent(
                event_type="page_view",
                event_data={"page": f"page-{i}"},
                user_id=f"user-{i % 10}"
            )
            for i in range(100)
        ]
        AnalyticsEvent.objects.bulk_create(events)
        
        end_time = time.time()
        duration = end_time - start_time
        
        assert AnalyticsEvent.objects.count() == 100
        assert duration < 1.0  # Should complete in under 1 second

    def test_metrics_query_performance(self):
        """Test metrics retrieval performance"""
        # Create metrics for multiple events
        metrics = [
            EventMetrics(
                event_id=f"event-{i}",
                total_views=100 * i,
                total_registrations=50 * i
            )
            for i in range(50)
        ]
        EventMetrics.objects.bulk_create(metrics)
        
        start_time = time.time()
        result = EventMetrics.objects.filter(event_id__startswith="event-").count()
        end_time = time.time()
        
        assert result == 50
        assert (end_time - start_time) < 0.5  # Should be fast


@pytest.mark.django_db
class TestDashboardPerformance:
    def test_user_analytics_bulk_query(self):
        """Test querying multiple user analytics efficiently"""
        # Create 100 users
        users = [
            UserAnalytics(
                user_id=f"user-{i}",
                total_events_attended=i,
                total_tickets_purchased=i * 2
            )
            for i in range(100)
        ]
        UserAnalytics.objects.bulk_create(users)
        
        start_time = time.time()
        all_users = list(UserAnalytics.objects.all())
        end_time = time.time()
        
        assert len(all_users) == 100
        assert (end_time - start_time) < 0.5

    def test_activity_tracking_performance(self):
        """Test activity tracking at scale"""
        start_time = time.time()
        
        # Create 200 activities
        activities = [
            UserActivity(
                user_id=f"user-{i % 20}",
                activity_type="event_view",
                event_id=f"event-{i % 10}"
            )
            for i in range(200)
        ]
        UserActivity.objects.bulk_create(activities)
        
        end_time = time.time()
        duration = end_time - start_time
        
        assert UserActivity.objects.count() == 200
        assert duration < 1.0
