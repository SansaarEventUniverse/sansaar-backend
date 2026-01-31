from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from application.services.personalization_service import PersonalizationService, PreferenceAnalysisService, ContentCustomizationService
from presentation.serializers.personalization_serializers import PersonalizationRuleSerializer, UserPreferenceSerializer, PersonalizeContentSerializer

@api_view(['POST'])
def personalize_content(request):
    serializer = PersonalizeContentSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    service = ContentCustomizationService()
    result = service.customize_for_user(
        serializer.validated_data['user_id'],
        serializer.validated_data['content']
    )
    
    return Response(result)

@api_view(['PUT'])
def update_preferences(request, user_id):
    service = PreferenceAnalysisService()
    preference = service.update_preference(user_id, request.data)
    
    return Response(UserPreferenceSerializer(preference).data)

@api_view(['GET'])
def get_personalization(request):
    service = PersonalizationService()
    rules = service.get_rules()
    serializer = PersonalizationRuleSerializer(rules, many=True)
    
    return Response(serializer.data)
