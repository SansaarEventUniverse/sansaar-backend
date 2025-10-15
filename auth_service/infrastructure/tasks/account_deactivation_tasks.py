from celery import shared_task
from django.utils import timezone

from domain.models import AccountDeactivation


@shared_task
def check_grace_periods():
    """Mark accounts as permanently deactivated after 30-day grace period"""
    expired_deactivations = AccountDeactivation.objects.filter(
        is_permanently_deactivated=False, grace_period_ends__lte=timezone.now()
    )

    marked_count = 0
    for deactivation in expired_deactivations:
        try:
            deactivation.mark_permanently_deactivated()
            marked_count += 1
        except Exception:
            pass  # Log error but continue

    return f"Marked {marked_count} accounts as permanently deactivated"
