from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from application.services.mentorship_service import MentorshipService, MentorMatchingService, MentorshipTrackingService
from infrastructure.repositories.mentorship_repository import MentorshipRepository
from presentation.serializers.mentorship_serializers import MentorshipProgramSerializer, MentorMenteeSerializer

@api_view(['POST'])
def create_program(request):
    serializer = MentorshipProgramSerializer(data=request.data)
    if serializer.is_valid():
        service = MentorshipService()
        program = service.create_program(serializer.validated_data)
        response_serializer = MentorshipProgramSerializer(program)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_programs(request):
    service = MentorshipService()
    programs = service.get_active_programs()
    serializer = MentorshipProgramSerializer(programs, many=True)
    return Response({'results': serializer.data})

@api_view(['POST'])
def join_program(request, program_id):
    mentor_user_id = request.data.get('mentor_user_id')
    mentee_user_id = request.data.get('mentee_user_id')
    
    if not mentor_user_id or not mentee_user_id:
        return Response({'error': 'mentor_user_id and mentee_user_id are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    service = MentorMatchingService()
    match = service.create_match(program_id, int(mentor_user_id), int(mentee_user_id))
    serializer = MentorMenteeSerializer(match)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_mentorships(request):
    user_id = request.query_params.get('user_id')
    role = request.query_params.get('role', 'mentee')
    
    if not user_id:
        return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    service = MentorshipTrackingService()
    if role == 'mentor':
        relationships = service.get_mentor_relationships(int(user_id))
    else:
        relationships = service.get_mentee_relationships(int(user_id))
    
    serializer = MentorMenteeSerializer(relationships, many=True)
    return Response({'results': serializer.data})
