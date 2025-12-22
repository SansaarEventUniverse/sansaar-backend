import pytest
from rest_framework.test import APIClient
from domain.models import AuditTrail, ComplianceReport


@pytest.mark.django_db
class TestAuditTrailAPI:
    def test_get_audit_trail(self):
        AuditTrail.objects.create(user_id="user-123", action="login", resource="auth")
        client = APIClient()
        response = client.get('/api/analytics/admin/audit-trail/?user_id=user-123')
        assert response.status_code == 200
        assert len(response.data) == 1

    def test_audit_search(self):
        AuditTrail.objects.create(user_id="user-123", action="login", resource="auth")
        client = APIClient()
        response = client.post('/api/analytics/admin/audit/search/', {
            'action': 'login'
        }, format='json')
        assert response.status_code == 200
        assert len(response.data) == 1


@pytest.mark.django_db
class TestComplianceAPI:
    def test_get_compliance_report(self):
        ComplianceReport.objects.create(report_type="gdpr", status="compliant")
        client = APIClient()
        response = client.get('/api/analytics/admin/compliance/')
        assert response.status_code == 200
        assert len(response.data) == 1
