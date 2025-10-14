class SearchAuditLogsService:
    def __init__(self, audit_search_service):
        self.audit_search_service = audit_search_service

    def search_logs(
        self,
        start_date: str = None,
        end_date: str = None,
        event_type: str = None,
        admin_id: str = None,
        page: int = 1,
        limit: int = 50,
    ) -> dict:
        return self.audit_search_service.search(
            start_date=start_date,
            end_date=end_date,
            event_type=event_type,
            admin_id=admin_id,
            page=page,
            limit=limit,
        )
