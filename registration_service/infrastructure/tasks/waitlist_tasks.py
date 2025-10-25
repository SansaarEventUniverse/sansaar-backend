from celery import shared_task
from application.waitlist_service import ProcessWaitlistService


@shared_task
def process_waitlists():
    """Process waitlists for events with available capacity."""
    # This would typically check events with available spots
    # and process their waitlists automatically
    return "Waitlist processing completed"
