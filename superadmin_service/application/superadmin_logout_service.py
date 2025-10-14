class SuperAdminLogoutService:
    def __init__(self, jwt_service, audit_logger=None):
        self.jwt_service = jwt_service
        self.audit_logger = audit_logger

    def logout(self, token: str, ip_address: str = None) -> dict:
        payload = self.jwt_service.verify_token(token)
        self.jwt_service.blacklist_token(token)

        if self.audit_logger and ip_address:
            self.audit_logger.log_superadmin_logout(payload.get("admin_id"), payload.get("email"), ip_address)

        return {"message": "Logged out successfully"}
