import re

from django.core.exceptions import ValidationError

from application.log_audit_event_service import LogAuditEventService
from application.tasks import delete_unverified_user
from domain.audit_log_model import AuditEventType
from domain.email_verification_token_model import EmailVerificationToken
from domain.user_model import User
from infrastructure.services.disposable_email_service import DisposableEmailService
from infrastructure.services.email_service import EmailService


class RegisterUserService:
    def __init__(self):
        self.disposable_email_service = DisposableEmailService()
        self.audit_service = LogAuditEventService()

    def register(self, data, ip_address=None, user_agent=None):
        self._validate_terms(data.get('agree_terms'))
        self._validate_passwords(data.get('password'), data.get('confirm_password'))
        self._validate_email(data.get('email'))

        user = User.objects.create_user(
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name']
        )

        # Log audit event
        self.audit_service.log_event(
            event_type=AuditEventType.REGISTRATION,
            user_id=str(user.id),
            ip_address=ip_address,
            user_agent=user_agent,
            metadata={'email': user.email}
        )

        # Create verification token and send email
        token = EmailVerificationToken.objects.create(user=user)
        email_service = EmailService()
        email_service.send_verification_email(
            to_email=user.email,
            verification_token=token.token,
            first_name=user.first_name
        )

        # Schedule deletion of unverified user after 10 minutes
        delete_unverified_user.apply_async(args=[user.id], countdown=600)

        return user

    def _validate_terms(self, agree_terms):
        if not agree_terms:
            raise ValidationError('You must agree to the terms and conditions')

    def _validate_passwords(self, password, confirm_password):
        if password != confirm_password:
            raise ValidationError('Passwords do not match')

        if len(password) < 8:
            raise ValidationError('Password must be at least 8 characters')

        if not re.search(r'[A-Z]', password):
            raise ValidationError('Password must contain at least one uppercase letter')

        if not re.search(r'[a-z]', password):
            raise ValidationError('Password must contain at least one lowercase letter')

        if not re.search(r'\d', password):
            raise ValidationError('Password must contain at least one number')

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError('Password must contain at least one special character')

    def _validate_email(self, email):
        if self.disposable_email_service.is_disposable(email):
            raise ValidationError('Disposable email addresses are not allowed')

        if User.objects.filter(email=email).exists():
            raise ValidationError('Email already registered')
