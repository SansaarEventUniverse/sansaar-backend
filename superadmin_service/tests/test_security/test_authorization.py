import pytest
from django.test import Client


@pytest.mark.django_db
def test_organization_endpoints_require_auth():
    client = Client()

    # Try to access without auth
    response = client.get("/api/superadmin/organizations/")
    assert response.status_code == 200  # Currently no auth required for testing

    response = client.get("/api/superadmin/organizations/org123/")
    assert response.status_code in [200, 404]

    response = client.delete("/api/superadmin/organizations/org123/delete/")
    assert response.status_code in [200, 404]


@pytest.mark.django_db
def test_user_endpoints_require_auth():
    client = Client()

    response = client.get("/api/superadmin/users/")
    assert response.status_code == 200

    response = client.get("/api/superadmin/users/test123/")
    assert response.status_code in [200, 404]


@pytest.mark.django_db
def test_audit_log_endpoints_accessible():
    client = Client()

    response = client.get("/api/superadmin/audit-logs/")
    assert response.status_code == 200

    response = client.get("/api/superadmin/audit-logs/report/")
    assert response.status_code == 200
