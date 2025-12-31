from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from domain.models import VolunteerOpportunity
from presentation.serializers.opportunity_serializers import VolunteerOpportunitySerializer
from application.services.create_opportunity_service import CreateOpportunityService

@api_view(['POST'])
def create_opportunity(request):
    serializer = VolunteerOpportunitySerializer(data=request.data)
    if serializer.is_valid():
        service = CreateOpportunityService()
        opportunity = service.create(serializer.validated_data)
        response_serializer = VolunteerOpportunitySerializer(opportunity)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_opportunities(request):
    opportunities = VolunteerOpportunity.objects.all().prefetch_related('skills')
    serializer = VolunteerOpportunitySerializer(opportunities, many=True)
    return Response({'results': serializer.data})

@api_view(['GET', 'PUT', 'PATCH'])
def manage_opportunity(request, opportunity_id):
    try:
        opportunity = VolunteerOpportunity.objects.prefetch_related('skills').get(id=opportunity_id)
    except VolunteerOpportunity.DoesNotExist:
        return Response({'error': 'Opportunity not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = VolunteerOpportunitySerializer(opportunity)
        return Response(serializer.data)
    
    serializer = VolunteerOpportunitySerializer(opportunity, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
