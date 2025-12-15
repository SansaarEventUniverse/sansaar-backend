from domain.models import UserAnalytics


class UserAnalyticsService:
    def calculate_engagement(self, user_id: str):
        analytics = UserAnalytics.objects.get(user_id=user_id)
        return {
            'user_id': analytics.user_id,
            'total_events_attended': analytics.total_events_attended,
            'total_tickets_purchased': analytics.total_tickets_purchased,
            'engagement_score': analytics.calculate_engagement_score()
        }
