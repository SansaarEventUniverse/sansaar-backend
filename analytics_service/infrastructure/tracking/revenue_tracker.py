from domain.models import RevenueAnalytics


class RevenueTracker:
    def track_revenue(self, event_id: str, revenue_type: str, amount):
        analytics, _ = RevenueAnalytics.objects.get_or_create(event_id=event_id)
        if revenue_type == "ticket":
            analytics.ticket_revenue += amount
        elif revenue_type == "sponsorship":
            analytics.sponsorship_revenue += amount
        analytics.save()
        return analytics
