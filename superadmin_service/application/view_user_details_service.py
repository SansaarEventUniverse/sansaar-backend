class ViewUserDetailsService:
    def __init__(self, user_management_service, audit_logger=None):
        self.user_management_service = user_management_service
        self.audit_logger = audit_logger

    def get_user(self, user_id: str, admin_id: str, admin_email: str) -> dict:
        user = self.user_management_service.get_user_by_id(user_id)

        if self.audit_logger:
            self.audit_logger.log_event(
                "SUPERADMIN_USER_VIEWED", admin_id, admin_email, "", {"viewed_user_id": user_id}
            )

        return user
