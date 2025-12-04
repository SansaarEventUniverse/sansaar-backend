from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError

from application.assign_org_role_service import AssignOrgRoleService
from application.revoke_org_role_service import RevokeOrgRoleService
from application.transfer_ownership_service import TransferOwnershipService
from application.check_org_permission_service import CheckOrgPermissionService
from infrastructure.cache.org_permission_cache_service import OrgPermissionCacheService
from presentation.serializers.org_role_serializers import (
    AssignOrgRoleSerializer,
    RevokeOrgRoleSerializer,
    TransferOwnershipSerializer,
    CheckOrgPermissionSerializer,
    OrgRoleResponseSerializer
)


class AssignOrgRoleView(APIView):
    def post(self, request, organization_id):
        serializer = AssignOrgRoleSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            service = AssignOrgRoleService()
            role = service.assign(
                organization_id,
                serializer.validated_data['user_id']
            )
            
            cache_service = OrgPermissionCacheService()
            cache_service.invalidate_user_cache(organization_id, serializer.validated_data['user_id'])
            
            response_serializer = OrgRoleResponseSerializer(role)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'error': e.messages if hasattr(e, 'messages') else str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RevokeOrgRoleView(APIView):
    def delete(self, request, organization_id):
        serializer = RevokeOrgRoleSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            service = RevokeOrgRoleService()
            service.revoke(organization_id, serializer.validated_data['user_id'])
            
            cache_service = OrgPermissionCacheService()
            cache_service.invalidate_user_cache(organization_id, serializer.validated_data['user_id'])
            
            return Response({'message': 'Role revoked successfully'}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'error': e.messages if hasattr(e, 'messages') else str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TransferOwnershipView(APIView):
    def post(self, request, organization_id):
        serializer = TransferOwnershipSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        current_owner_id = request.data.get('current_owner_id')
        if not current_owner_id:
            return Response({'error': 'current_owner_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            service = TransferOwnershipService()
            new_owner = service.transfer(
                organization_id,
                current_owner_id,
                serializer.validated_data['new_owner_id']
            )
            
            cache_service = OrgPermissionCacheService()
            cache_service.invalidate_org_cache(organization_id)
            
            response_serializer = OrgRoleResponseSerializer(new_owner)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'error': e.messages if hasattr(e, 'messages') else str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CheckOrgPermissionView(APIView):
    def get(self, request, organization_id):
        serializer = CheckOrgPermissionSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user_id = serializer.validated_data['user_id']
        resource = serializer.validated_data['resource']
        action = serializer.validated_data['action']
        
        cache_service = OrgPermissionCacheService()
        cached_result = cache_service.get_cached_permission(organization_id, user_id)
        
        if cached_result is not None:
            return Response({'has_permission': cached_result, 'cached': True})
        
        service = CheckOrgPermissionService()
        has_permission = service.check(organization_id, user_id, resource, action)
        
        cache_service.cache_permission(organization_id, user_id, has_permission)
        
        return Response({'has_permission': has_permission, 'cached': False})
