import uuid
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from application.recommendation_service import (
    EventRecommendationService,
    UserPreferenceService,
    SimilarEventsService,
)
from presentation.serializers.recommendation_serializers import (
    UpdatePreferencesSerializer,
    UserPreferenceSerializer,
)
from presentation.serializers.search_serializers import EventSearchResultSerializer


@api_view(['GET'])
def get_recommendations(request):
    """Get personalized event recommendations."""
    user_id = request.GET.get('user_id')
    if not user_id:
        return Response(
            {'error': 'user_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        return Response(
            {'error': 'Invalid user_id'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    limit = int(request.GET.get('limit', 10))
    
    service = EventRecommendationService()
    recommendations = service.generate_recommendations(user_uuid, limit=limit)
    
    return Response({
        'recommendations': recommendations,
        'count': len(recommendations)
    })


@api_view(['GET', 'POST'])
def manage_preferences(request, user_id):
    """Get or update user preferences."""
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        return Response(
            {'error': 'Invalid user_id'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    service = UserPreferenceService()
    
    if request.method == 'GET':
        pref = service.get_or_create_preference(user_uuid)
        return Response(UserPreferenceSerializer(pref).data)
    
    elif request.method == 'POST':
        serializer = UpdatePreferencesSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        pref = service.update_preferences(user_uuid, serializer.validated_data)
        return Response(UserPreferenceSerializer(pref).data)


@api_view(['GET'])
def get_similar_events(request, event_id):
    """Get events similar to given event."""
    try:
        event_uuid = uuid.UUID(event_id)
    except ValueError:
        return Response(
            {'error': 'Invalid event_id'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    limit = int(request.GET.get('limit', 5))
    
    service = SimilarEventsService()
    similar = service.find_similar(event_uuid, limit=limit)
    
    return Response({
        'similar_events': EventSearchResultSerializer(similar, many=True).data,
        'count': len(similar)
    })
