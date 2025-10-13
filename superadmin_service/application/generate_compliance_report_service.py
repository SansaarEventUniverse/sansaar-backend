import csv
from io import StringIO


class GenerateComplianceReportService:
    def __init__(self, audit_search_service):
        self.audit_search_service = audit_search_service

    def generate_report(self, start_date: str = None, end_date: str = None, event_type: str = None) -> str:
        logs = self.audit_search_service.search(
            start_date=start_date, end_date=end_date, event_type=event_type, page=1, limit=10000
        )

        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["Timestamp", "Event Type", "Admin ID", "Email", "IP Address", "Metadata"])

        for log in logs.get("logs", []):
            writer.writerow(
                [
                    log.get("timestamp"),
                    log.get("event_type"),
                    log.get("admin_id"),
                    log.get("email"),
                    log.get("ip_address"),
                    str(log.get("metadata", {})),
                ]
            )

        return output.getvalue()
