from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from application.deactivate_user_service import DeactivateUserService
from application.list_all_users_service import ListAllUsersService
from application.view_user_details_service import ViewUserDetailsService
from infrastructure.audit.audit_logger import AuditLogger
from infrastructure.services.user_management_service import UserManagementService
from presentation.serializers.user_serializers import (
    DeactivateUserResponseSerializer,
    UserListResponseSerializer,
    UserSerializer,
)


@api_view(["GET"])
def list_users(request):
    page = int(request.GET.get("page", 1))
    limit = int(request.GET.get("limit", 50))

    user_mgmt_service = UserManagementService()
    service = ListAllUsersService(user_mgmt_service)

    try:
        result = service.list_users(page, limit)
        serializer = UserListResponseSerializer(result)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def view_user(request, user_id):
    admin_id = getattr(request, "superadmin_id", "")
    admin_email = getattr(request, "superadmin_email", "")

    user_mgmt_service = UserManagementService()
    audit_logger = AuditLogger()
    service = ViewUserDetailsService(user_mgmt_service, audit_logger)

    try:
        result = service.get_user(user_id, admin_id, admin_email)
        serializer = UserSerializer(result)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def deactivate_user(request, user_id):
    admin_id = getattr(request, "superadmin_id", "")
    admin_email = getattr(request, "superadmin_email", "")

    user_mgmt_service = UserManagementService()
    audit_logger = AuditLogger()
    service = DeactivateUserService(user_mgmt_service, audit_logger)

    try:
        result = service.deactivate_user(user_id, admin_id, admin_email)
        serializer = DeactivateUserResponseSerializer(result)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
