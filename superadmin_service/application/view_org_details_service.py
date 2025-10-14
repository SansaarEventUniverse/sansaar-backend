from infrastructure.audit.audit_logger import AuditLogger


class ViewOrgDetailsService:
    def __init__(self, org_management_service, audit_logger: AuditLogger):
        self.org_management_service = org_management_service
        self.audit_logger = audit_logger

    def view_organization(self, org_id: str, admin_id: str, admin_email: str, ip_address: str = "127.0.0.1") -> dict:
        org = self.org_management_service.get_organization_by_id(org_id)

        self.audit_logger.log_event(
            event_type="SUPERADMIN_ORG_VIEWED",
            admin_id=admin_id,
            email=admin_email,
            ip_address=ip_address,
            metadata={"org_id": org_id},
        )

        return org
