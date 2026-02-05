from rest_framework.decorators import api_view
from rest_framework.response import Response
from application.services.journey_service import CustomerJourneyService, JourneyMappingService, JourneyAnalysisService
from domain.models import CustomerJourney
from presentation.serializers.journey_serializers import CustomerJourneySerializer

@api_view(['GET'])
def get_customer_journey(request, journey_id):
    try:
        journey = CustomerJourney.objects.get(id=journey_id)
        serializer = CustomerJourneySerializer(journey)
        return Response(serializer.data)
    except CustomerJourney.DoesNotExist:
        return Response({'error': 'Journey not found'}, status=404)

@api_view(['POST'])
def map_journey(request):
    service = JourneyMappingService()
    result = service.map_journey(
        journey_id=request.data.get('journey_id'),
        stages=request.data.get('stages', [])
    )
    return Response(result)

@api_view(['GET'])
def journey_analysis(request):
    user_id = request.query_params.get('user_id')
    if not user_id:
        return Response({'error': 'user_id required'}, status=400)
    service = JourneyAnalysisService()
    result = service.analyze_journey(int(user_id))
    return Response(result)
