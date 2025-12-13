import pytest
from decimal import Decimal
from domain.models import EventMetrics, AttendanceAnalytics
from infrastructure.repositories.event_analytics_repository import EventAnalyticsRepository
from infrastructure.tracking.attendance_tracker import AttendanceTracker
from infrastructure.calculation.metrics_calculator import MetricsCalculator


@pytest.mark.django_db
class TestEventAnalyticsRepository:
    def test_save_metrics(self):
        repo = EventAnalyticsRepository()
        metrics = repo.save_metrics("event-123", total_views=10)
        assert metrics.event_id == "event-123"
        assert metrics.total_views == 10

    def test_get_metrics(self):
        EventMetrics.objects.create(event_id="event-123", total_views=50)
        repo = EventAnalyticsRepository()
        metrics = repo.get_metrics("event-123")
        assert metrics.total_views == 50


@pytest.mark.django_db
class TestAttendanceTracker:
    def test_track_check_in(self):
        tracker = AttendanceTracker()
        attendance = tracker.track_check_in("event-123", "user-456")
        assert attendance.is_checked_in is True

    def test_track_check_out(self):
        AttendanceAnalytics.objects.create(
            event_id="event-123",
            user_id="user-456",
            check_in_time="2024-01-01T10:00:00Z",
            is_checked_in=True
        )
        tracker = AttendanceTracker()
        attendance = tracker.track_check_out("event-123", "user-456")
        assert attendance.is_checked_in is False


@pytest.mark.django_db
class TestMetricsCalculator:
    def test_calculate_conversion_rate(self):
        EventMetrics.objects.create(
            event_id="event-123",
            total_views=100,
            total_registrations=50
        )
        calculator = MetricsCalculator()
        rate = calculator.calculate_conversion_rate("event-123")
        assert rate == 50.0

    def test_calculate_attendance_rate(self):
        EventMetrics.objects.create(
            event_id="event-123",
            total_registrations=50,
            total_attendance=30
        )
        calculator = MetricsCalculator()
        rate = calculator.calculate_attendance_rate("event-123")
        assert rate == 60.0
