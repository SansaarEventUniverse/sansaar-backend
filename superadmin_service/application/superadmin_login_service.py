import bcrypt
from django.core.exceptions import ValidationError
from django.utils import timezone

from domain.superadmin_model import SuperAdmin


class SuperAdminLoginService:
    def __init__(self, ip_whitelist_service, jwt_service):
        self.ip_whitelist_service = ip_whitelist_service
        self.jwt_service = jwt_service

    def login(self, email: str, password: str, mfa_token: str, ip_address: str) -> dict:
        if not self.ip_whitelist_service.is_whitelisted(ip_address):
            raise ValidationError("IP address not whitelisted")

        try:
            admin = SuperAdmin.objects.get(email=email)
        except SuperAdmin.DoesNotExist:
            raise ValidationError("Invalid credentials")

        admin.validate_active()

        if not bcrypt.checkpw(password.encode(), admin.password_hash.encode()):
            raise ValidationError("Invalid credentials")

        if not admin.verify_mfa(mfa_token):
            raise ValidationError("Invalid MFA token")

        admin.last_login = timezone.now()
        admin.save(update_fields=["last_login"])

        token = self.jwt_service.generate_token(str(admin.id), admin.email)
        return {"token": token, "admin_id": str(admin.id), "email": admin.email}
