from django.http import JsonResponse
from rest_framework.decorators import api_view

from application.delete_organization_service import DeleteOrganizationService
from application.list_all_organizations_service import ListAllOrganizationsService
from application.view_org_details_service import ViewOrgDetailsService
from infrastructure.audit.audit_logger import AuditLogger
from infrastructure.services.org_management_service import OrgManagementService
from presentation.serializers.organization_serializers import OrganizationSerializer


@api_view(["GET"])
def list_organizations(request):
    page = int(request.GET.get("page", 1))
    limit = int(request.GET.get("limit", 50))

    org_service = OrgManagementService()
    service = ListAllOrganizationsService(org_service)

    result = service.list_organizations(page, limit)
    return JsonResponse(result)


@api_view(["GET"])
def view_organization(request, org_id):
    org_service = OrgManagementService()
    audit_logger = AuditLogger()
    service = ViewOrgDetailsService(org_service, audit_logger)

    admin_id = getattr(request, "admin_id", "test_admin")
    admin_email = getattr(request, "admin_email", "test@admin.com")

    try:
        org = service.view_organization(org_id, admin_id, admin_email)
        serializer = OrganizationSerializer(org)
        return JsonResponse(serializer.data)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=404)


@api_view(["DELETE"])
def delete_organization(request, org_id):
    org_service = OrgManagementService()
    audit_logger = AuditLogger()
    service = DeleteOrganizationService(org_service, audit_logger)

    admin_id = getattr(request, "admin_id", "test_admin")
    admin_email = getattr(request, "admin_email", "test@admin.com")

    try:
        result = service.delete_organization(org_id, admin_id, admin_email)
        return JsonResponse(result)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=404)
