import uuid
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError

from application.group_service import (
    CreateGroupRegistrationService,
    AddGroupMemberService,
    ConfirmGroupRegistrationService,
    CancelGroupRegistrationService,
)
from domain.group_registration import GroupRegistration
from infrastructure.services.group_analytics_service import GroupAnalyticsService
from presentation.serializers.group_serializers import (
    GroupRegistrationSerializer,
    CreateGroupSerializer,
    JoinGroupSerializer,
)


@api_view(['POST'])
def create_group(request, event_id):
    """Create group registration."""
    serializer = CreateGroupSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        service = CreateGroupRegistrationService()
        data = {**serializer.validated_data, 'event_id': event_id}
        group = service.execute(data)
        return Response(
            GroupRegistrationSerializer(group).data,
            status=status.HTTP_201_CREATED
        )
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def join_group(request, event_id, group_id):
    """Join a group."""
    serializer = JoinGroupSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        service = AddGroupMemberService()
        member = service.execute(
            uuid.UUID(group_id),
            serializer.validated_data['user_id'],
            serializer.validated_data['name'],
            serializer.validated_data['email'],
        )
        return Response(
            {'id': str(member.id), 'message': 'Successfully joined group'},
            status=status.HTTP_201_CREATED
        )
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_group(request, event_id, group_id):
    """Get group details."""
    try:
        group = GroupRegistration.objects.prefetch_related('members').get(id=group_id)
        return Response(GroupRegistrationSerializer(group).data)
    except GroupRegistration.DoesNotExist:
        return Response({'error': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def confirm_group(request, event_id, group_id):
    """Confirm group registration."""
    try:
        service = ConfirmGroupRegistrationService()
        group = service.execute(uuid.UUID(group_id))
        return Response(GroupRegistrationSerializer(group).data)
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def cancel_group(request, event_id, group_id):
    """Cancel group registration."""
    try:
        service = CancelGroupRegistrationService()
        group = service.execute(uuid.UUID(group_id))
        return Response(GroupRegistrationSerializer(group).data)
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_group_stats(request, event_id):
    """Get group statistics for event."""
    service = GroupAnalyticsService()
    stats = service.get_group_stats(uuid.UUID(event_id))
    return Response(stats)
