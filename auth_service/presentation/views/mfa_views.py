from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from application.disable_mfa_service import DisableMFAService
from application.enable_mfa_service import EnableMFAService
from application.verify_mfa_service import VerifyMFAService
from presentation.serializers.auth_serializers import VerifyMFASerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def enable_mfa(request):
    try:
        service = EnableMFAService()
        result = service.enable_mfa(request.user)
        return Response(result, status=status.HTTP_200_OK)
    except Exception:
        return Response({"error": "Failed to enable MFA"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def verify_mfa(request):
    serializer = VerifyMFASerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        service = VerifyMFAService()
        service.verify_mfa(request.user, serializer.validated_data["code"])
        return Response({"message": "MFA verified successfully"}, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response({"error": str(e.message)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def disable_mfa(request):
    try:
        service = DisableMFAService()
        service.disable_mfa(request.user)
        return Response({"message": "MFA disabled successfully"}, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response({"error": str(e.message)}, status=status.HTTP_400_BAD_REQUEST)
