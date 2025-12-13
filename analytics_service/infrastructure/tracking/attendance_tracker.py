from django.utils import timezone
from domain.models import AttendanceAnalytics


class AttendanceTracker:
    def track_check_in(self, event_id: str, user_id: str) -> AttendanceAnalytics:
        attendance, _ = AttendanceAnalytics.objects.get_or_create(
            event_id=event_id,
            user_id=user_id,
            defaults={'check_in_time': timezone.now(), 'is_checked_in': True}
        )
        return attendance

    def track_check_out(self, event_id: str, user_id: str) -> AttendanceAnalytics:
        attendance = AttendanceAnalytics.objects.get(event_id=event_id, user_id=user_id)
        attendance.check_out(timezone.now())
        return attendance
