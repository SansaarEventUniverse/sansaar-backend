from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from application.superadmin_login_service import SuperAdminLoginService
from application.superadmin_logout_service import SuperAdminLogoutService
from infrastructure.services.ip_whitelist_service import IPWhitelistService
from infrastructure.services.jwt_service import JWTService
from presentation.serializers.auth_serializers import (
    SuperAdminLoginResponseSerializer,
    SuperAdminLoginSerializer,
    SuperAdminLogoutSerializer,
)


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


@api_view(["POST"])
def superadmin_login(request):
    serializer = SuperAdminLoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    ip_address = get_client_ip(request)
    ip_service = IPWhitelistService()
    jwt_service = JWTService()
    login_service = SuperAdminLoginService(ip_service, jwt_service)

    try:
        result = login_service.login(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
            mfa_token=serializer.validated_data["mfa_token"],
            ip_address=ip_address,
        )
        response_serializer = SuperAdminLoginResponseSerializer(result)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["POST"])
def superadmin_logout(request):
    auth_header = request.META.get("HTTP_AUTHORIZATION")
    if not auth_header or not auth_header.startswith("Bearer "):
        return Response({"error": "Authorization header required"}, status=status.HTTP_401_UNAUTHORIZED)

    token = auth_header.split(" ")[1]
    jwt_service = JWTService()
    logout_service = SuperAdminLogoutService(jwt_service)

    result = logout_service.logout(token)
    response_serializer = SuperAdminLogoutSerializer(result)
    return Response(response_serializer.data, status=status.HTTP_200_OK)
