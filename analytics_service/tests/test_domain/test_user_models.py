import pytest
from django.core.exceptions import ValidationError
from domain.models import UserAnalytics, UserActivity


@pytest.mark.django_db
class TestUserAnalytics:
    def test_create_user_analytics(self):
        analytics = UserAnalytics.objects.create(
            user_id="user-123",
            total_events_attended=5,
            total_tickets_purchased=10
        )
        assert analytics.user_id == "user-123"
        assert analytics.total_events_attended == 5

    def test_calculate_engagement_score(self):
        analytics = UserAnalytics.objects.create(
            user_id="user-123",
            total_events_attended=5,
            total_tickets_purchased=10
        )
        score = analytics.calculate_engagement_score()
        assert score == 15

    def test_user_id_required(self):
        analytics = UserAnalytics(total_events_attended=5)
        with pytest.raises(ValidationError):
            analytics.full_clean()


@pytest.mark.django_db
class TestUserActivity:
    def test_create_user_activity(self):
        activity = UserActivity.objects.create(
            user_id="user-123",
            activity_type="event_view",
            event_id="event-456"
        )
        assert activity.user_id == "user-123"
        assert activity.activity_type == "event_view"

    def test_get_user_activities(self):
        UserActivity.objects.create(user_id="user-123", activity_type="event_view")
        UserActivity.objects.create(user_id="user-123", activity_type="ticket_purchase")
        activities = UserActivity.get_user_activities("user-123")
        assert activities.count() == 2
