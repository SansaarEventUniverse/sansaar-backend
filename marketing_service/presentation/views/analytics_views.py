from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from application.services.analytics_service import CampaignAnalyticsService, ReportGenerationService
from presentation.serializers.analytics_serializers import CampaignAnalyticsSerializer

@api_view(['GET'])
def get_campaign_analytics(request, campaign_id):
    service = CampaignAnalyticsService()
    analytics = service.get_analytics(campaign_id)
    
    if not analytics:
        return Response({'error': 'Analytics not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = CampaignAnalyticsSerializer(analytics)
    return Response(serializer.data)

@api_view(['POST'])
def generate_report(request, campaign_id):
    service = ReportGenerationService()
    report = service.generate_report(campaign_id)
    
    return Response(report)
