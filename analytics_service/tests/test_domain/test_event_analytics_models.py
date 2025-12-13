import pytest
from django.core.exceptions import ValidationError
from domain.models import EventMetrics, AttendanceAnalytics


@pytest.mark.django_db
class TestEventMetrics:
    def test_create_event_metrics(self):
        metrics = EventMetrics.objects.create(
            event_id='event_123',
            total_views=100,
            total_registrations=50,
            total_attendance=45
        )
        assert metrics.event_id == 'event_123'
        assert metrics.total_views == 100

    def test_event_id_validation(self):
        metrics = EventMetrics(event_id='', total_views=10)
        with pytest.raises(ValidationError):
            metrics.full_clean()

    def test_calculate_conversion_rate(self):
        metrics = EventMetrics.objects.create(
            event_id='event_123',
            total_views=100,
            total_registrations=50
        )
        assert metrics.calculate_conversion_rate() == 50.0

    def test_calculate_attendance_rate(self):
        metrics = EventMetrics.objects.create(
            event_id='event_123',
            total_registrations=50,
            total_attendance=45
        )
        assert metrics.calculate_attendance_rate() == 90.0

    def test_get_metrics_by_event(self):
        EventMetrics.objects.create(event_id='event_123', total_views=100)
        metrics = EventMetrics.get_metrics_by_event('event_123')
        assert metrics is not None


@pytest.mark.django_db
class TestAttendanceAnalytics:
    def test_create_attendance(self):
        attendance = AttendanceAnalytics.objects.create(
            event_id='event_123',
            user_id='user_456',
            check_in_time='2026-02-07T10:00:00Z'
        )
        assert attendance.event_id == 'event_123'
        assert attendance.is_checked_in is True

    def test_event_id_validation(self):
        attendance = AttendanceAnalytics(event_id='', user_id='user_123')
        with pytest.raises(ValidationError):
            attendance.full_clean()

    def test_check_out(self):
        attendance = AttendanceAnalytics.objects.create(
            event_id='event_123',
            user_id='user_456',
            check_in_time='2026-02-07T10:00:00Z'
        )
        attendance.check_out('2026-02-07T12:00:00Z')
        assert attendance.check_out_time is not None
        assert attendance.is_checked_in is False

    def test_get_event_attendance(self):
        AttendanceAnalytics.objects.create(event_id='event_123', user_id='user_1', check_in_time='2026-02-07T10:00:00Z')
        AttendanceAnalytics.objects.create(event_id='event_123', user_id='user_2', check_in_time='2026-02-07T10:00:00Z')
        assert AttendanceAnalytics.get_event_attendance('event_123').count() == 2
