from django.core.exceptions import ValidationError


class DeactivateUserService:
    def __init__(self, user_management_service, audit_logger=None):
        self.user_management_service = user_management_service
        self.audit_logger = audit_logger

    def deactivate_user(self, user_id: str, admin_id: str, admin_email: str) -> dict:
        user = self.user_management_service.get_user_by_id(user_id)

        if not user.get("is_active"):
            raise ValidationError("User is already deactivated")

        result = self.user_management_service.deactivate_user(user_id)

        if self.audit_logger:
            self.audit_logger.log_event(
                "SUPERADMIN_USER_DEACTIVATED", admin_id, admin_email, "", {"deactivated_user_id": user_id}
            )

        return result
