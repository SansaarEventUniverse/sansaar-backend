from django.core.exceptions import ValidationError

from application.log_audit_event_service import LogAuditEventService
from domain.audit_log_model import AuditEventType
from domain.refresh_token_model import RefreshToken


class LogoutService:
    def __init__(self):
        self.audit_service = LogAuditEventService()

    def logout(self, refresh_token, ip_address=None, user_agent=None):
        try:
            token = RefreshToken.objects.get(token=refresh_token)
        except RefreshToken.DoesNotExist:
            raise ValidationError('Invalid refresh token')

        if token.is_blacklisted:
            raise ValidationError('Token already blacklisted')

        if token.is_expired():
            raise ValidationError('Token has expired')

        token.blacklist()

        # Log logout event
        self.audit_service.log_event(
            event_type=AuditEventType.LOGOUT,
            user_id=str(token.user.id),
            ip_address=ip_address,
            user_agent=user_agent,
            metadata={'email': token.user.email}
        )

        return True
