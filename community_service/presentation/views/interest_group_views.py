from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from application.services.interest_group_service import InterestGroupService, GroupMembershipService, GroupModerationService
from infrastructure.repositories.interest_group_repository import InterestGroupRepository
from presentation.serializers.interest_group_serializers import InterestGroupSerializer, GroupMembershipSerializer

@api_view(['POST'])
def create_group(request):
    serializer = InterestGroupSerializer(data=request.data)
    if serializer.is_valid():
        service = InterestGroupService()
        group = service.create_group(serializer.validated_data)
        response_serializer = InterestGroupSerializer(group)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_groups(request):
    category = request.query_params.get('category')
    service = InterestGroupService()
    
    if category:
        groups = service.get_groups_by_category(category)
    else:
        groups = service.get_active_groups()
    
    serializer = InterestGroupSerializer(groups, many=True)
    return Response({'results': serializer.data})

@api_view(['POST'])
def join_group(request, group_id):
    user_id = request.data.get('user_id')
    
    if not user_id:
        return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        service = GroupMembershipService()
        membership = service.join_group(group_id, int(user_id))
        serializer = GroupMembershipSerializer(membership)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_recommendations(request):
    user_id = request.query_params.get('user_id')
    
    if not user_id:
        return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    repo = InterestGroupRepository()
    recommendations = repo.get_group_recommendations(int(user_id), limit=5)
    serializer = InterestGroupSerializer(recommendations, many=True)
    return Response({'recommendations': serializer.data})
