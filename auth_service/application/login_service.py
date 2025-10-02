from django.core.exceptions import ValidationError

from application.create_session_service import CreateSessionService
from application.log_audit_event_service import LogAuditEventService
from application.verify_mfa_service import VerifyMFAService
from domain.audit_log_model import AuditEventType
from domain.login_attempt_model import LoginAttempt
from domain.refresh_token_model import RefreshToken
from domain.user_model import User
from infrastructure.services.jwt_service import JWTService


class LoginService:
    def __init__(self):
        self.audit_service = LogAuditEventService()
        self.mfa_service = VerifyMFAService()
        self.session_service = CreateSessionService()

    def execute(self, email, password, mfa_code=None, ip_address=None, user_agent=None):
        """Execute login with lockout protection"""
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            self.audit_service.log_event(
                event_type=AuditEventType.LOGIN,
                user_id=email,
                ip_address=ip_address,
                user_agent=user_agent,
                success=False,
                metadata={'reason': 'User not found'}
            )
            return {'success': False, 'error': 'Invalid email or password'}

        # Check if account is locked
        if user.is_locked_out():
            self.audit_service.log_event(
                event_type=AuditEventType.ACCOUNT_LOCKED,
                user_id=str(user.id),
                ip_address=ip_address,
                user_agent=user_agent,
                success=False,
                metadata={'reason': 'Account locked due to failed login attempts'}
            )
            return {'success': False, 'error': 'Account is locked due to too many failed login attempts. Please try again later.'}

        if not user.check_password(password):
            # Record failed attempt
            LoginAttempt.objects.create(
                user=user,
                ip_address=ip_address,
                success=False
            )
            
            self.audit_service.log_event(
                event_type=AuditEventType.LOGIN,
                user_id=str(user.id),
                ip_address=ip_address,
                user_agent=user_agent,
                success=False,
                metadata={'reason': 'Invalid password'}
            )
            return {'success': False, 'error': 'Invalid email or password'}

        if not user.is_email_verified:
            return {'success': False, 'error': 'Email not verified'}

        if not user.is_active:
            return {'success': False, 'error': 'Account is inactive'}

        # Check if MFA is enabled
        if user.has_mfa_enabled():
            if not mfa_code:
                return {'success': True, 'mfa_required': True, 'user_id': str(user.id)}

            # Verify MFA code
            try:
                self.mfa_service.verify_mfa(user, mfa_code)
            except ValidationError as e:
                return {'success': False, 'error': str(e)}

        # Reset login attempts on successful login
        user.reset_login_attempts()

        # Create session
        session = self.session_service.execute(
            user=user,
            ip_address=ip_address,
            user_agent=user_agent
        )

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
            metadata={'email': user.email, 'session_id': str(session.id)}
        )

        return {
            'success': True,
            'access_token': access_token,
            'refresh_token': refresh_token_jwt,
            'session_id': str(session.id),
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        }

    def login(self, email, password, mfa_code=None, ip_address=None, user_agent=None):
        """Legacy method for backward compatibility"""
        result = self.execute(email, password, mfa_code, ip_address, user_agent)
        
        if not result.get('success'):
            raise ValidationError(result.get('error', 'Login failed'))
        
        # Return old format
        if result.get('mfa_required'):
            return {'mfa_required': True, 'user_id': result['user_id']}
        
        return {
            'access_token': result['access_token'],
            'refresh_token': result['refresh_token'],
            'user': result['user']
        }
