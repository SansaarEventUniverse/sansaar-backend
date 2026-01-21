from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from application.services.email_campaign_service import EmailCampaignService, CampaignSchedulingService
from presentation.serializers.email_campaign_serializers import EmailCampaignSerializer

@api_view(['POST', 'GET'])
def campaigns(request):
    """Create or get campaigns"""
    service = EmailCampaignService()
    
    if request.method == 'POST':
        campaign = service.create_campaign(request.data)
        serializer = EmailCampaignSerializer(campaign)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    campaigns = service.get_campaigns()
    serializer = EmailCampaignSerializer(campaigns, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def send_campaign(request, campaign_id):
    """Send campaign"""
    service = CampaignSchedulingService()
    recipients = request.data.get('recipients', [])
    result = service.send_campaign(campaign_id, recipients)
    
    if result:
        campaign = EmailCampaignService().get_campaign(campaign_id)
        serializer = EmailCampaignSerializer(campaign)
        return Response(serializer.data)
    return Response({'error': 'Failed to send campaign'}, status=status.HTTP_400_BAD_REQUEST)
