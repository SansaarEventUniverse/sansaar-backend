from rest_framework.decorators import api_view
from rest_framework.response import Response
from application.services.roi_service import ROIAnalyticsService, ROICalculationService, ROIReportingService
from presentation.serializers.roi_serializers import ROIAnalyticsSerializer

@api_view(['GET'])
def get_roi_analytics(request):
    campaign_id = request.query_params.get('campaign_id')
    if not campaign_id:
        return Response({'error': 'campaign_id required'}, status=400)
    service = ROIAnalyticsService()
    analytics = service.get_roi_analytics(int(campaign_id))
    serializer = ROIAnalyticsSerializer(analytics, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def calculate_roi(request):
    service = ROICalculationService()
    result = service.calculate_roi(
        campaign_id=request.data.get('campaign_id'),
        revenue=request.data.get('revenue'),
        cost=request.data.get('cost')
    )
    return Response(result)

@api_view(['GET'])
def roi_report(request):
    campaign_id = request.query_params.get('campaign_id')
    if not campaign_id:
        return Response({'error': 'campaign_id required'}, status=400)
    service = ROIReportingService()
    result = service.generate_report(int(campaign_id))
    return Response(result)
