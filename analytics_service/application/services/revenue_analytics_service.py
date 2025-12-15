from django.db import transaction
from domain.models import RevenueAnalytics


class RevenueAnalyticsService:
    @transaction.atomic
    def track_ticket_revenue(self, event_id: str, amount):
        analytics, _ = RevenueAnalytics.objects.get_or_create(event_id=event_id)
        analytics.ticket_revenue += amount
        analytics.save()
        return analytics

    @transaction.atomic
    def track_sponsorship_revenue(self, event_id: str, amount):
        analytics, _ = RevenueAnalytics.objects.get_or_create(event_id=event_id)
        analytics.sponsorship_revenue += amount
        analytics.save()
        return analytics
