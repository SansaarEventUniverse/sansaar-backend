from domain.models import ROIAnalytics, ROIMetric

class ROIAnalyticsService:
    def get_roi_analytics(self, campaign_id):
        return ROIAnalytics.objects.filter(campaign_id=campaign_id)

class ROICalculationService:
    def calculate_roi(self, campaign_id, revenue, cost):
        roi = ROIAnalytics.objects.create(
            campaign_id=campaign_id,
            revenue=revenue,
            cost=cost,
            roi_data={}
        )
        return {'campaign_id': campaign_id, 'roi': roi.calculate_roi(), 'profit': roi.get_profit()}

class ROIReportingService:
    def generate_report(self, campaign_id):
        analytics = ROIAnalytics.objects.filter(campaign_id=campaign_id).first()
        if not analytics:
            return {'campaign_id': campaign_id, 'status': 'no data'}
        return {
            'campaign_id': campaign_id,
            'revenue': analytics.revenue,
            'cost': analytics.cost,
            'roi': analytics.calculate_roi(),
            'profit': analytics.get_profit()
        }
