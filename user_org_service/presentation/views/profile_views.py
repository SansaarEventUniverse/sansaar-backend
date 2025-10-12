from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from application.get_profile_service import GetProfileService
from application.list_profiles_service import ListProfilesService
from application.update_profile_service import UpdateProfileService
from application.upload_profile_picture_service import UploadProfilePictureService
from presentation.serializers.profile_serializers import (
    UpdateProfileSerializer,
    UploadProfilePictureSerializer,
    UserProfileSerializer,
)


@api_view(["GET"])
@permission_classes([AllowAny])
def list_profiles(request):
    page = int(request.GET.get("page", 1))
    limit = int(request.GET.get("limit", 50))
    service = ListProfilesService()
    result = service.list_profiles(page, limit)
    return Response(result, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_profile(request, user_id):
    try:
        service = GetProfileService()
        profile = service.get_profile(user_id)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response({"error": str(e.message)}, status=status.HTTP_404_NOT_FOUND)


@api_view(["PUT"])
@permission_classes([AllowAny])
def update_profile(request, user_id):
    serializer = UpdateProfileSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        service = UpdateProfileService()
        profile = service.update_profile(user_id, **serializer.validated_data)
        profile_serializer = UserProfileSerializer(profile)
        return Response(profile_serializer.data, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response({"error": str(e.message)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def upload_profile_picture(request, user_id):
    serializer = UploadProfilePictureSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        service = UploadProfilePictureService()
        profile = service.upload(user_id, serializer.validated_data["file"])
        profile_serializer = UserProfileSerializer(profile)
        return Response(profile_serializer.data, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response({"error": str(e.message)}, status=status.HTTP_400_BAD_REQUEST)
