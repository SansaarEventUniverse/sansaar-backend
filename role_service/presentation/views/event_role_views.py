from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.core.exceptions import ValidationError

from application.assign_event_role_service import AssignEventRoleService
from application.revoke_event_role_service import RevokeEventRoleService
from application.check_event_permission_service import CheckEventPermissionService
from infrastructure.cache.permission_cache_service import PermissionCacheService
from presentation.serializers.event_role_serializers import (
    AssignEventRoleSerializer,
    RevokeEventRoleSerializer,
    CheckEventPermissionSerializer,
    EventRoleResponseSerializer
)


@api_view(['POST'])
@permission_classes([AllowAny])
def assign_event_role(request, event_id):
    serializer = AssignEventRoleSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        service = AssignEventRoleService()
        role = service.execute(
            event_id=event_id,
            user_id=serializer.validated_data['user_id'],
            role=serializer.validated_data['role']
        )

        cache_service = PermissionCacheService()
        cache_service.invalidate_user_cache(event_id, serializer.validated_data['user_id'])

        response_serializer = EventRoleResponseSerializer(role)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([AllowAny])
def revoke_event_role(request, event_id):
    serializer = RevokeEventRoleSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    service = RevokeEventRoleService()
    result = service.execute(
        event_id=event_id,
        user_id=serializer.validated_data['user_id']
    )

    if not result:
        return Response({'error': 'Role not found'}, status=status.HTTP_404_NOT_FOUND)

    cache_service = PermissionCacheService()
    cache_service.invalidate_user_cache(event_id, serializer.validated_data['user_id'])

    return Response({'message': 'Role revoked successfully'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def check_event_permission(request, event_id):
    serializer = CheckEventPermissionSerializer(data=request.query_params)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user_id = serializer.validated_data['user_id']
    resource = serializer.validated_data['resource']
    action = serializer.validated_data['action']

    cache_service = PermissionCacheService()
    cached = cache_service.get_cached_permission(event_id, user_id)

    if cached is not None:
        return Response({'has_permission': cached, 'cached': True}, status=status.HTTP_200_OK)

    service = CheckEventPermissionService()
    has_permission = service.execute(
        event_id=event_id,
        user_id=user_id,
        resource=resource,
        action=action
    )

    cache_service.cache_permission(event_id, user_id, has_permission)

    return Response({'has_permission': has_permission, 'cached': False}, status=status.HTTP_200_OK)
