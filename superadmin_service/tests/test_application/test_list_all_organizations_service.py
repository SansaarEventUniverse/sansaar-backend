import pytest

from application.list_all_organizations_service import ListAllOrganizationsService
from infrastructure.services.org_management_service import OrgManagementService


@pytest.mark.django_db
def test_list_organizations():
    org_service = OrgManagementService()
    service = ListAllOrganizationsService(org_service)

    result = service.list_organizations(page=1, limit=50)

    assert "organizations" in result
    assert "total" in result
    assert "page" in result
    assert "limit" in result


@pytest.mark.django_db
def test_list_organizations_with_pagination():
    org_service = OrgManagementService()
    service = ListAllOrganizationsService(org_service)

    result = service.list_organizations(page=2, limit=10)

    assert result["page"] == 2
    assert result["limit"] == 10
