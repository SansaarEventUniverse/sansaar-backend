from rest_framework.decorators import api_view
from rest_framework.response import Response
from application.services.intelligence_service import MarketingIntelligenceService, InsightGenerationService, PredictiveAnalyticsService
from presentation.serializers.intelligence_serializers import MarketingIntelligenceSerializer

@api_view(['GET'])
def get_intelligence(request):
    service = MarketingIntelligenceService()
    campaign_id = request.query_params.get('campaign_id')
    if campaign_id:
        intelligence = service.get_intelligence(int(campaign_id))
        serializer = MarketingIntelligenceSerializer(intelligence, many=True)
        return Response(serializer.data)
    return Response([])

@api_view(['POST'])
def generate_insights(request):
    campaign_id = request.data.get('campaign_id')
    service = InsightGenerationService()
    insights = service.generate_insights(campaign_id)
    return Response(insights)

@api_view(['GET'])
def predictive_analytics(request, campaign_id):
    service = PredictiveAnalyticsService()
    prediction = service.predict(campaign_id)
    return Response(prediction)
