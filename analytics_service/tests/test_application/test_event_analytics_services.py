import pytest
from decimal import Decimal
from django.utils import timezone
from domain.models import EventMetrics, AttendanceAnalytics
from application.services.event_analytics_service import EventAnalyticsService
from application.services.attendance_tracking_service import AttendanceTrackingService
from application.services.metrics_reporting_service import MetricsReportingService


@pytest.mark.django_db
class TestEventAnalyticsService:
    def test_track_event_view(self):
        service = EventAnalyticsService()
        metrics = service.track_event_view("event-123")
        assert metrics.event_id == "event-123"
        assert metrics.total_views == 1

    def test_track_event_registration(self):
        service = EventAnalyticsService()
        metrics = service.track_event_registration("event-123")
        assert metrics.total_registrations == 1

    def test_update_revenue(self):
        service = EventAnalyticsService()
        metrics = service.update_revenue("event-123", Decimal("100.00"))
        assert metrics.revenue == Decimal("100.00")


@pytest.mark.django_db
class TestAttendanceTrackingService:
    def test_check_in_user(self):
        service = AttendanceTrackingService()
        attendance = service.check_in_user("event-123", "user-456")
        assert attendance.event_id == "event-123"
        assert attendance.user_id == "user-456"
        assert attendance.is_checked_in is True

    def test_check_out_user(self):
        service = AttendanceTrackingService()
        attendance = service.check_in_user("event-123", "user-456")
        updated = service.check_out_user("event-123", "user-456")
        assert updated.is_checked_in is False
        assert updated.check_out_time is not None

    def test_get_attendance_count(self):
        service = AttendanceTrackingService()
        service.check_in_user("event-123", "user-1")
        service.check_in_user("event-123", "user-2")
        count = service.get_attendance_count("event-123")
        assert count == 2


@pytest.mark.django_db
class TestMetricsReportingService:
    def test_get_event_metrics(self):
        EventMetrics.objects.create(
            event_id="event-123",
            total_views=100,
            total_registrations=50,
            total_attendance=30,
            revenue=Decimal("1000.00")
        )
        service = MetricsReportingService()
        metrics = service.get_event_metrics("event-123")
        assert metrics["total_views"] == 100
        assert metrics["conversion_rate"] == 50.0
        assert metrics["attendance_rate"] == 60.0

    def test_export_metrics_csv(self):
        EventMetrics.objects.create(event_id="event-123", total_views=100)
        service = MetricsReportingService()
        csv_data = service.export_metrics("event-123", "csv")
        assert "event_id" in csv_data
        assert "event-123" in csv_data

    def test_export_metrics_json(self):
        EventMetrics.objects.create(event_id="event-123", total_views=100)
        service = MetricsReportingService()
        json_data = service.export_metrics("event-123", "json")
        assert "event_id" in json_data
