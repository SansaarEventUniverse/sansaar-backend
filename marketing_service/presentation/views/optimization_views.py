from rest_framework.decorators import api_view
from rest_framework.response import Response
from application.services.optimization_service import CampaignOptimizationService, AutoOptimizationService
from domain.models import CampaignOptimization
from presentation.serializers.optimization_serializers import CampaignOptimizationSerializer

@api_view(['POST'])
def optimize_campaign(request, campaign_id):
    service = CampaignOptimizationService()
    result = service.optimize_campaign(
        campaign_id=campaign_id,
        optimization_type=request.data.get('optimization_type', 'general'),
        current_metrics=request.data.get('current_metrics', {}),
        target_metrics=request.data.get('target_metrics', {})
    )
    return Response(result)

@api_view(['GET'])
def get_optimization(request, campaign_id):
    optimizations = CampaignOptimization.objects.filter(campaign_id=campaign_id)
    serializer = CampaignOptimizationSerializer(optimizations, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def auto_optimize(request, campaign_id):
    service = AutoOptimizationService()
    metrics = request.data.get('metrics', {})
    result = service.auto_optimize(campaign_id, metrics)
    return Response(result)
