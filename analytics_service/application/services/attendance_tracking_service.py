from django.db import transaction
from django.utils import timezone
from domain.models import AttendanceAnalytics, EventMetrics


class AttendanceTrackingService:
    @transaction.atomic
    def check_in_user(self, event_id: str, user_id: str) -> AttendanceAnalytics:
        attendance, created = AttendanceAnalytics.objects.get_or_create(
            event_id=event_id,
            user_id=user_id,
            defaults={'check_in_time': timezone.now(), 'is_checked_in': True}
        )
        if not created and not attendance.is_checked_in:
            attendance.check_in_time = timezone.now()
            attendance.is_checked_in = True
            attendance.save()
        
        metrics, _ = EventMetrics.objects.get_or_create(event_id=event_id)
        metrics.total_attendance = AttendanceAnalytics.objects.filter(
            event_id=event_id, is_checked_in=True
        ).count()
        metrics.save()
        
        return attendance

    @transaction.atomic
    def check_out_user(self, event_id: str, user_id: str) -> AttendanceAnalytics:
        attendance = AttendanceAnalytics.objects.get(event_id=event_id, user_id=user_id)
        attendance.check_out(timezone.now())
        return attendance

    def get_attendance_count(self, event_id: str) -> int:
        return AttendanceAnalytics.objects.filter(event_id=event_id).count()
