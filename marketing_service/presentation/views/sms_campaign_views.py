from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from application.services.sms_campaign_service import SMSCampaignService, SMSDeliveryService
from presentation.serializers.sms_campaign_serializers import SMSCampaignSerializer, SendSMSSerializer

@api_view(['GET', 'POST'])
def sms_campaign_list_create(request):
    service = SMSCampaignService()
    
    if request.method == 'GET':
        campaigns = service.get_campaigns()
        serializer = SMSCampaignSerializer(campaigns, many=True)
        return Response(serializer.data)
    
    serializer = SMSCampaignSerializer(data=request.data)
    if serializer.is_valid():
        campaign = service.create_campaign(serializer.validated_data)
        return Response(SMSCampaignSerializer(campaign).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def send_sms_campaign(request, campaign_id):
    serializer = SendSMSSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    service = SMSDeliveryService()
    service.send_campaign(campaign_id, serializer.validated_data['phone_numbers'])
    
    return Response({'status': 'SMS campaign sent'})
