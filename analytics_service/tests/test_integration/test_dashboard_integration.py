import pytest
from domain.models import Dashboard, DashboardWidget, UserAnalytics, UserActivity


@pytest.mark.django_db
class TestDashboardIntegration:
    def test_dashboard_with_widgets(self):
        """Test dashboard creation with multiple widgets"""
        dashboard = Dashboard.objects.create(
            organizer_id="org-123",
            name="Main Dashboard"
        )
        
        # Add widgets
        DashboardWidget.objects.create(
            dashboard=dashboard,
            widget_type="chart",
            config={"type": "bar"}
        )
        DashboardWidget.objects.create(
            dashboard=dashboard,
            widget_type="metric",
            config={"metric": "revenue"}
        )
        
        widgets = DashboardWidget.objects.filter(dashboard=dashboard)
        assert widgets.count() == 2


@pytest.mark.django_db
class TestUserAnalyticsIntegration:
    def test_user_activity_tracking_flow(self):
        """Test complete user activity tracking workflow"""
        # Create user analytics
        analytics = UserAnalytics.objects.create(
            user_id="user-123",
            total_events_attended=0,
            total_tickets_purchased=0
        )
        
        # Track activities
        UserActivity.objects.create(
            user_id="user-123",
            activity_type="event_view",
            event_id="event-456"
        )
        UserActivity.objects.create(
            user_id="user-123",
            activity_type="ticket_purchase",
            event_id="event-456"
        )
        
        # Update analytics
        analytics.total_events_attended = 1
        analytics.total_tickets_purchased = 1
        analytics.save()
        
        activities = UserActivity.get_user_activities("user-123")
        assert len(list(activities)) == 2
        assert analytics.calculate_engagement_score() == 2

    def test_multi_user_repository(self):
        """Test repository with multiple users"""
        UserAnalytics.objects.create(user_id="user-1", total_events_attended=5)
        UserAnalytics.objects.create(user_id="user-2", total_events_attended=3)
        UserAnalytics.objects.create(user_id="user-3", total_events_attended=8)
        
        users = UserAnalytics.objects.all()
        assert users.count() == 3
