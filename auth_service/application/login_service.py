from django.core.exceptions import ValidationError

from application.log_audit_event_service import LogAuditEventService
from application.verify_mfa_service import VerifyMFAService
from domain.audit_log_model import AuditEventType
from domain.refresh_token_model import RefreshToken
from domain.user_model import User
from infrastructure.services.jwt_service import JWTService


class LoginService:
    def __init__(self):
        self.audit_service = LogAuditEventService()
        self.mfa_service = VerifyMFAService()

    def login(self, email, password, mfa_code=None, ip_address=None, user_agent=None):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Log failed login
            self.audit_service.log_event(
                event_type=AuditEventType.LOGIN,
                user_id=email,
                ip_address=ip_address,
                user_agent=user_agent,
                success=False,
                metadata={'reason': 'User not found'}
            )
            raise ValidationError('Invalid email or password')

        if not user.check_password(password):
            # Log failed login
            self.audit_service.log_event(
                event_type=AuditEventType.LOGIN,
                user_id=str(user.id),
                ip_address=ip_address,
                user_agent=user_agent,
                success=False,
                metadata={'reason': 'Invalid password'}
            )
            raise ValidationError('Invalid email or password')

        if not user.is_email_verified:
            raise ValidationError('Email not verified')

        if not user.is_active:
            raise ValidationError('Account is inactive')

        # Check if MFA is enabled
        if user.has_mfa_enabled():
            if not mfa_code:
                return {'mfa_required': True, 'user_id': str(user.id)}

            # Verify MFA code
            self.mfa_service.verify_mfa(user, mfa_code)

        # Generate tokens
        jwt_service = JWTService()
        access_token = jwt_service.generate_access_token(user)
        refresh_token_jwt = jwt_service.generate_refresh_token(user)

        # Store refresh token in database
        RefreshToken.objects.create(user=user)

        # Log successful login
        self.audit_service.log_event(
            event_type=AuditEventType.LOGIN,
            user_id=str(user.id),
            ip_address=ip_address,
            user_agent=user_agent,
            metadata={'email': user.email}
        )

        return {
            'access_token': access_token,
            'refresh_token': refresh_token_jwt,
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        }
