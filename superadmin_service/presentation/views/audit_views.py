from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view

from application.generate_compliance_report_service import GenerateComplianceReportService
from application.search_audit_logs_service import SearchAuditLogsService
from infrastructure.audit.audit_logger import AuditLogger
from infrastructure.services.audit_log_search_service import AuditLogSearchService


@api_view(["GET"])
def search_audit_logs(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    event_type = request.GET.get("event_type")
    admin_id = request.GET.get("admin_id")
    page = int(request.GET.get("page", 1))
    limit = int(request.GET.get("limit", 50))

    search_service = AuditLogSearchService()
    service = SearchAuditLogsService(search_service)

    result = service.search_logs(
        start_date=start_date, end_date=end_date, event_type=event_type, admin_id=admin_id, page=page, limit=limit
    )

    # Log the search
    audit_logger = AuditLogger()
    current_admin_id = getattr(request, "admin_id", "test_admin")
    current_admin_email = getattr(request, "admin_email", "test@admin.com")
    ip_address = request.META.get("REMOTE_ADDR", "127.0.0.1")

    audit_logger.log_event(
        event_type="SUPERADMIN_AUDIT_LOG_SEARCHED",
        admin_id=current_admin_id,
        email=current_admin_email,
        ip_address=ip_address,
        metadata={"filters": {"start_date": start_date, "end_date": end_date, "event_type": event_type}},
    )

    return JsonResponse(result)


@api_view(["GET"])
def generate_report(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    event_type = request.GET.get("event_type")

    search_service = AuditLogSearchService()
    service = GenerateComplianceReportService(search_service)

    csv_content = service.generate_report(start_date=start_date, end_date=end_date, event_type=event_type)

    # Log the report generation
    audit_logger = AuditLogger()
    current_admin_id = getattr(request, "admin_id", "test_admin")
    current_admin_email = getattr(request, "admin_email", "test@admin.com")
    ip_address = request.META.get("REMOTE_ADDR", "127.0.0.1")

    audit_logger.log_event(
        event_type="SUPERADMIN_REPORT_GENERATED",
        admin_id=current_admin_id,
        email=current_admin_email,
        ip_address=ip_address,
        metadata={"filters": {"start_date": start_date, "end_date": end_date, "event_type": event_type}},
    )

    response = HttpResponse(csv_content, content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="audit_report.csv"'
    return response
