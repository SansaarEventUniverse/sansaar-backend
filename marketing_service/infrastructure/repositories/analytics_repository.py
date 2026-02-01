from domain.models import CampaignAnalytics

class AnalyticsRepository:
    def get_campaign_stats(self):
        total = CampaignAnalytics.objects.count()
        return {'total_campaigns_tracked': total}
