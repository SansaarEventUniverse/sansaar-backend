from domain.models import AttributionModel, TouchPoint

class AttributionService:
    def create_attribution(self, campaign_id, model_type, conversion_value, attribution_data):
        return AttributionModel.objects.create(
            campaign_id=campaign_id,
            model_type=model_type,
            conversion_value=conversion_value,
            attribution_data=attribution_data
        )

class TouchPointTrackingService:
    def track_touchpoint(self, campaign_id, channel, user_id, touchpoint_data):
        return TouchPoint.objects.create(
            campaign_id=campaign_id,
            channel=channel,
            user_id=user_id,
            touchpoint_data=touchpoint_data
        )

class AttributionAnalysisService:
    def analyze_attribution(self, campaign_id):
        touchpoints = TouchPoint.objects.filter(campaign_id=campaign_id)
        channels = list(set([tp.channel for tp in touchpoints]))
        return {'campaign_id': campaign_id, 'total_touchpoints': touchpoints.count(), 'channels': channels}
