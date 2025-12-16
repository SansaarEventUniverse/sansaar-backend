from django.db import transaction
from domain.models import UserAnalytics


class UserAnalyticsPipeline:
    @transaction.atomic
    def update_user_analytics(self, user_id: str, events_attended: int = 0, tickets_purchased: int = 0):
        analytics, _ = UserAnalytics.objects.get_or_create(user_id=user_id)
        analytics.total_events_attended += events_attended
        analytics.total_tickets_purchased += tickets_purchased
        analytics.save()
        return analytics
