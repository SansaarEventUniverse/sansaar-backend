from allauth.socialaccount.models import SocialAccount
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from application.change_password_service import ChangePasswordService
from application.login_service import LoginService
from application.register_user_service import RegisterUserService
from application.request_password_reset_service import RequestPasswordResetService
from application.resend_verification_service import ResendVerificationService
from application.reset_password_service import ResetPasswordService
from application.verify_email_service import VerifyEmailService
from infrastructure.oauth.google_adapter import GoogleOAuthAdapter
from presentation.serializers.auth_serializers import (
    ChangePasswordSerializer,
    LoginSerializer,
    RegisterUserSerializer,
    RequestPasswordResetSerializer,
    ResendVerificationSerializer,
    ResetPasswordSerializer,
    UserSerializer,
)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterUserSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        service = RegisterUserService()
        user = service.register(serializer.validated_data)

        user_serializer = UserSerializer(user)
        return Response({
            'message': 'User registered successfully',
            'user': user_serializer.data
        }, status=status.HTTP_201_CREATED)
    except ValidationError as e:
        return Response({'non_field_errors': [str(e.message)]}, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response({'error': 'Registration failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        service = LoginService()
        result = service.login(
            serializer.validated_data['email'],
            serializer.validated_data['password']
        )
        return Response(result, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response({'error': str(e.message)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response({'error': 'Login failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def request_password_reset(request):
    serializer = RequestPasswordResetSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        service = RequestPasswordResetService()
        service.request_reset(serializer.validated_data['email'])
        return Response({'message': 'Password reset email sent'}, status=status.HTTP_200_OK)
    except Exception:
        return Response({'error': 'Failed to send password reset email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    serializer = ResetPasswordSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        service = ResetPasswordService()
        service.reset_password(
            serializer.validated_data['token'],
            serializer.validated_data['new_password']
        )
        return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response({'error': str(e.message)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response({'error': 'Password reset failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def google_callback(request):
    try:
        # Get user from social account
        uid = request.GET.get('uid')
        if not uid:
            return Response({'error': 'Missing uid parameter'}, status=status.HTTP_400_BAD_REQUEST)

        social_account = SocialAccount.objects.get(provider='google', uid=uid)
        user = social_account.user

        # Generate JWT tokens
        adapter = GoogleOAuthAdapter()
        tokens = adapter.generate_tokens(user)

        return Response({
            **tokens,
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        }, status=status.HTTP_200_OK)
    except SocialAccount.DoesNotExist:
        return Response({'error': 'Social account not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return Response({'error': 'OAuth callback failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def verify_email(request, token):
    try:
        service = VerifyEmailService()
        service.verify(token)
        return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response({'error': str(e.message)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response({'error': 'Verification failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def resend_verification(request):
    serializer = ResendVerificationSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        service = ResendVerificationService()
        service.resend(serializer.validated_data['email'])
        return Response({'message': 'Verification email sent successfully'}, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response({'error': str(e.message)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response({'error': 'Failed to send verification email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    serializer = ChangePasswordSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        service = ChangePasswordService()
        service.change_password(
            user=request.user,
            current_password=serializer.validated_data['current_password'],
            new_password=serializer.validated_data['new_password']
        )
        return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response({'error': str(e.message)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response({'error': 'Password change failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

