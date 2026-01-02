from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from domain.models import VolunteerApplication
from presentation.serializers.application_serializers import VolunteerApplicationSerializer
from application.services.application_service import ApplicationService

@api_view(['POST'])
def apply_for_opportunity(request, opportunity_id):
    data = request.data.copy()
    data['opportunity_id'] = opportunity_id
    service = ApplicationService()
    application = service.create(data)
    serializer = VolunteerApplicationSerializer(application)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_applications(request):
    applications = VolunteerApplication.objects.all().select_related('opportunity')
    serializer = VolunteerApplicationSerializer(applications, many=True)
    return Response({'results': serializer.data})

@api_view(['GET', 'PATCH'])
def manage_application(request, application_id):
    try:
        application = VolunteerApplication.objects.select_related('opportunity').get(id=application_id)
    except VolunteerApplication.DoesNotExist:
        return Response({'error': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = VolunteerApplicationSerializer(application)
        return Response(serializer.data)
    
    serializer = VolunteerApplicationSerializer(application, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
