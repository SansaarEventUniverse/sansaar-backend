from domain.models import CampaignAnalytics, PerformanceMetric

class CampaignAnalyticsService:
    def get_analytics(self, campaign_id):
        return CampaignAnalytics.objects.filter(campaign_id=campaign_id).first()

    def create_analytics(self, data):
        return CampaignAnalytics.objects.create(**data)

class PerformanceTrackingService:
    def track_metric(self, campaign_id, metric_name, metric_value):
        return PerformanceMetric.objects.create(
            campaign_id=campaign_id,
            metric_name=metric_name,
            metric_value=metric_value
        )

class ReportGenerationService:
    def generate_report(self, campaign_id):
        analytics = CampaignAnalytics.objects.filter(campaign_id=campaign_id).first()
        if not analytics:
            return {'error': 'No analytics found'}
        
        return {
            'campaign_id': campaign_id,
            'open_rate': analytics.calculate_open_rate(),
            'click_rate': analytics.calculate_click_rate(),
            'total_sent': analytics.total_sent,
            'total_delivered': analytics.total_delivered
        }
