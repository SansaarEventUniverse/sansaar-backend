from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from domain.models import Feedback
from presentation.serializers.feedback_serializers import FeedbackSerializer
from application.services.feedback_service import FeedbackService
from infrastructure.repositories.feedback_repository import FeedbackRepository

@api_view(['POST'])
def submit_feedback(request):
    serializer = FeedbackSerializer(data=request.data)
    if serializer.is_valid():
        service = FeedbackService()
        feedback = service.create(serializer.validated_data)
        response_serializer = FeedbackSerializer(feedback)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_feedback(request):
    feedback_type = request.query_params.get('type')
    entity_id = request.query_params.get('entity_id')
    
    if not feedback_type or not entity_id:
        return Response({'error': 'type and entity_id are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    service = FeedbackService()
    feedbacks = service.get_by_entity(feedback_type, int(entity_id))
    serializer = FeedbackSerializer(feedbacks, many=True)
    return Response({'results': serializer.data})

@api_view(['GET'])
def feedback_analytics(request):
    feedback_type = request.query_params.get('type')
    entity_id = request.query_params.get('entity_id')
    
    if not feedback_type or not entity_id:
        return Response({'error': 'type and entity_id are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    repo = FeedbackRepository()
    stats = repo.get_feedback_stats(feedback_type, int(entity_id))
    return Response(stats)
