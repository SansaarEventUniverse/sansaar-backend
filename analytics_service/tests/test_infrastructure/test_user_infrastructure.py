import pytest
from domain.models import UserAnalytics, UserActivity
from infrastructure.repositories.user_repository import UserRepository
from infrastructure.pipeline.user_analytics_pipeline import UserAnalyticsPipeline
from infrastructure.tracking.user_activity_tracker import UserActivityTracker


@pytest.mark.django_db
class TestUserRepository:
    def test_get_all_users(self):
        UserAnalytics.objects.create(user_id="user-1", total_events_attended=5)
        UserAnalytics.objects.create(user_id="user-2", total_events_attended=3)
        repo = UserRepository()
        users = repo.get_all_users()
        assert len(users) == 2


@pytest.mark.django_db
class TestUserAnalyticsPipeline:
    def test_update_user_analytics(self):
        UserAnalytics.objects.create(user_id="user-123", total_events_attended=5)
        pipeline = UserAnalyticsPipeline()
        pipeline.update_user_analytics("user-123", events_attended=2)
        analytics = UserAnalytics.objects.get(user_id="user-123")
        assert analytics.total_events_attended == 7


@pytest.mark.django_db
class TestUserActivityTracker:
    def test_track_user_activity(self):
        tracker = UserActivityTracker()
        activity = tracker.track("user-123", "event_view", "event-456")
        assert activity.activity_type == "event_view"
