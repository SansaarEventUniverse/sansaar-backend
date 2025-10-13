from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from application.delete_organization_service import DeleteOrganizationService
from application.get_organization_service import GetOrganizationService
from application.list_organizations_service import ListOrganizationsService


@require_http_methods(["GET"])
def list_organizations(request):
    page = int(request.GET.get("page", 1))
    limit = int(request.GET.get("limit", 50))

    service = ListOrganizationsService()
    result = service.list_organizations(page, limit)
    return JsonResponse(result)


@require_http_methods(["GET"])
def get_organization(request, org_id):
    service = GetOrganizationService()
    try:
        result = service.get_organization(org_id)
        return JsonResponse(result)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=404)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_organization(request, org_id):
    service = DeleteOrganizationService()
    try:
        result = service.delete_organization(org_id)
        return JsonResponse(result)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=404)
