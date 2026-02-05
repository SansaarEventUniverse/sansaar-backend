from rest_framework.decorators import api_view
from rest_framework.response import Response
from application.services.attribution_service import AttributionService, TouchPointTrackingService, AttributionAnalysisService
from domain.models import AttributionModel
from presentation.serializers.attribution_serializers import AttributionModelSerializer

@api_view(['GET'])
def get_attribution(request, attribution_id):
    try:
        attribution = AttributionModel.objects.get(id=attribution_id)
        serializer = AttributionModelSerializer(attribution)
        return Response(serializer.data)
    except AttributionModel.DoesNotExist:
        return Response({'error': 'Attribution not found'}, status=404)

@api_view(['POST'])
def track_touchpoint(request):
    service = TouchPointTrackingService()
    touchpoint = service.track_touchpoint(
        campaign_id=request.data.get('campaign_id'),
        channel=request.data.get('channel'),
        user_id=request.data.get('user_id'),
        touchpoint_data=request.data.get('touchpoint_data', {})
    )
    return Response({'id': touchpoint.id, 'channel': touchpoint.channel})

@api_view(['GET'])
def attribution_analysis(request):
    campaign_id = request.query_params.get('campaign_id')
    if not campaign_id:
        return Response({'error': 'campaign_id required'}, status=400)
    service = AttributionAnalysisService()
    result = service.analyze_attribution(int(campaign_id))
    return Response(result)
