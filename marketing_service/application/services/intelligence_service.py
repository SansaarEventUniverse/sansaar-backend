from domain.models import MarketingIntelligence, IntelligenceInsight

class MarketingIntelligenceService:
    def get_intelligence(self, campaign_id):
        return MarketingIntelligence.objects.filter(campaign_id=campaign_id)

    def create_intelligence(self, data):
        return MarketingIntelligence.objects.create(**data)

class InsightGenerationService:
    def generate_insights(self, campaign_id):
        intelligence = MarketingIntelligence.objects.filter(campaign_id=campaign_id).first()
        if intelligence:
            return intelligence.generate_insights()
        return {"insights": "no data"}

class PredictiveAnalyticsService:
    def predict(self, campaign_id):
        return {"campaign_id": campaign_id, "prediction": "positive", "confidence": 0.85}
