from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from application.deactivate_account_service import DeactivateAccountService
from application.delete_account_service import DeleteAccountService
from application.reactivate_account_service import ReactivateAccountService


@api_view(["POST"])
@permission_classes([AllowAny])
def deactivate_account(request, user_id):
    try:
        reason = request.data.get("reason")
        service = DeactivateAccountService()
        result = service.deactivate(user_id, reason)
        return Response(result, status=status.HTTP_200_OK)
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
@permission_classes([AllowAny])
def reactivate_account(request, user_id):
    try:
        is_superadmin = request.data.get("is_superadmin", False)
        service = ReactivateAccountService()
        result = service.reactivate(user_id, is_superadmin)
        return Response(result, status=status.HTTP_200_OK)
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([AllowAny])
def delete_account(request, user_id):
    try:
        service = DeleteAccountService()
        result = service.delete(user_id)
        return Response(result, status=status.HTTP_200_OK)
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
