import pytest
from django.utils import timezone
from domain.models import AnalyticsEvent, EventMetrics, AttendanceAnalytics


@pytest.mark.django_db
class TestAnalyticsPipelineIntegration:
    def test_event_creation_and_retrieval(self):
        """Test event creation and retrieval"""
        event = AnalyticsEvent.objects.create(
            event_type="page_view",
            event_data={"page": "home"},
            user_id="user-123"
        )
        
        assert AnalyticsEvent.objects.count() == 1
        retrieved = AnalyticsEvent.objects.get(id=event.id)
        assert retrieved.event_type == "page_view"

    def test_event_metrics_creation(self):
        """Test event metrics creation and retrieval"""
        metrics = EventMetrics.objects.create(
            event_id="event-123",
            total_views=100,
            total_registrations=50
        )
        
        retrieved = EventMetrics.objects.get(event_id="event-123")
        assert retrieved.total_views == 100
        assert retrieved.total_registrations == 50


@pytest.mark.django_db
class TestAttendanceTrackingIntegration:
    def test_check_in_check_out_flow(self):
        """Test complete check-in/check-out workflow"""
        check_in_time = timezone.now()
        attendance = AttendanceAnalytics.objects.create(
            event_id="event-123",
            user_id="user-123",
            is_checked_in=True,
            check_in_time=check_in_time
        )
        
        # Check out
        attendance.check_out_time = timezone.now()
        attendance.save()
        
        assert attendance.is_checked_in is True
        assert attendance.check_out_time >= attendance.check_in_time
