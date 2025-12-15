import pytest
from domain.models import UserAnalytics, UserActivity
from application.services.user_management_service import UserManagementService
from application.services.user_activity_service import UserActivityService
from application.services.user_analytics_service import UserAnalyticsService


@pytest.mark.django_db
class TestUserManagementService:
    def test_get_user_analytics(self):
        UserAnalytics.objects.create(user_id="user-123", total_events_attended=5)
        service = UserManagementService()
        analytics = service.get_user_analytics("user-123")
        assert analytics.user_id == "user-123"


@pytest.mark.django_db
class TestUserActivityService:
    def test_track_activity(self):
        service = UserActivityService()
        activity = service.track_activity("user-123", "event_view", "event-456")
        assert activity.activity_type == "event_view"

    def test_get_user_activities(self):
        service = UserActivityService()
        service.track_activity("user-123", "event_view")
        activities = service.get_user_activities("user-123")
        assert len(activities) == 1


@pytest.mark.django_db
class TestUserAnalyticsService:
    def test_calculate_engagement(self):
        UserAnalytics.objects.create(
            user_id="user-123",
            total_events_attended=5,
            total_tickets_purchased=10
        )
        service = UserAnalyticsService()
        engagement = service.calculate_engagement("user-123")
        assert engagement['engagement_score'] == 15
