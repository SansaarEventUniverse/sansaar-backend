import bcrypt
from django.core.exceptions import ValidationError
from django.utils import timezone

from domain.superadmin_model import SuperAdmin


class SuperAdminLoginService:
    def __init__(self, ip_whitelist_service, jwt_service, audit_logger=None):
        self.ip_whitelist_service = ip_whitelist_service
        self.jwt_service = jwt_service
        self.audit_logger = audit_logger

    def login(self, email: str, password: str, mfa_token: str, ip_address: str) -> dict:
        if not self.ip_whitelist_service.is_whitelisted(ip_address):
            if self.audit_logger:
                self.audit_logger.log_ip_whitelist_violation(email, ip_address)
            raise ValidationError("IP address not whitelisted")

        try:
            admin = SuperAdmin.objects.get(email=email)
        except SuperAdmin.DoesNotExist:
            if self.audit_logger:
                self.audit_logger.log_superadmin_login_failed(email, ip_address, "Invalid credentials")
            raise ValidationError("Invalid credentials")

        admin.validate_active()

        if not bcrypt.checkpw(password.encode(), admin.password_hash.encode()):
            if self.audit_logger:
                self.audit_logger.log_superadmin_login_failed(email, ip_address, "Invalid password")
            raise ValidationError("Invalid credentials")

        if not admin.verify_mfa(mfa_token):
            if self.audit_logger:
                self.audit_logger.log_superadmin_login_failed(email, ip_address, "Invalid MFA token")
            raise ValidationError("Invalid MFA token")

        admin.last_login = timezone.now()
        admin.save(update_fields=["last_login"])

        token = self.jwt_service.generate_token(str(admin.id), admin.email)

        if self.audit_logger:
            self.audit_logger.log_superadmin_login(str(admin.id), admin.email, ip_address)

        return {"token": token, "admin_id": str(admin.id), "email": admin.email}
