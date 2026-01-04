from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from domain.models import EventFeedback
from presentation.serializers.feedback_serializers import EventFeedbackSerializer
from application.services.feedback_service import FeedbackService, RatingAnalysisService

@api_view(['POST'])
def submit_feedback(request, event_id):
    data = request.data.copy()
    data['event_id'] = event_id
    serializer = EventFeedbackSerializer(data=data)
    if serializer.is_valid():
        service = FeedbackService()
        feedback = service.create(serializer.validated_data)
        response_serializer = EventFeedbackSerializer(feedback)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_feedback(request, event_id):
    service = FeedbackService()
    feedbacks = service.get_by_event(event_id)
    serializer = EventFeedbackSerializer(feedbacks, many=True)
    return Response({'results': serializer.data})

@api_view(['GET'])
def feedback_analytics(request, event_id):
    service = RatingAnalysisService()
    avg_rating = service.calculate_average_rating(event_id)
    feedbacks = EventFeedback.objects.filter(event_id=event_id, status='approved')
    return Response({
        'average_rating': avg_rating,
        'total_feedback': feedbacks.count(),
        'positive_count': feedbacks.filter(rating__gte=4).count(),
        'negative_count': feedbacks.filter(rating__lte=2).count()
    })
