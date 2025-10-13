import pytest

from infrastructure.services.org_management_service import OrgManagementService


@pytest.mark.django_db
def test_get_organizations():
    service = OrgManagementService()
    result = service.get_organizations(page=1, limit=50)

    assert "organizations" in result
    assert "total" in result


@pytest.mark.django_db
def test_get_organization_by_id():
    service = OrgManagementService()

    try:
        result = service.get_organization_by_id("org123")
        assert "org_id" in result
    except ValueError as e:
        assert "not found" in str(e)


@pytest.mark.django_db
def test_delete_organization_not_found():
    service = OrgManagementService()

    with pytest.raises(ValueError) as exc:
        service.delete_organization("nonexistent")
    assert "not found" in str(exc.value)
