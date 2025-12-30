import pytest
from rest_framework.test import APIClient
from domain.models import SecurityEvent, SecurityRule


@pytest.mark.django_db
class TestSecurityMonitoringAPI:
    def test_get_security_events(self):
        SecurityEvent.objects.create(event_type="attack", severity="high", source_ip="1.1.1.1", description="Test")
        client = APIClient()
        response = client.get('/api/superadmin/admin/security-events/')
        assert response.status_code == 200
        assert len(response.data) == 1

    def test_security_dashboard(self):
        SecurityEvent.objects.create(event_type="attack", severity="critical", source_ip="1.1.1.1", description="Test")
        client = APIClient()
        response = client.get('/api/superadmin/admin/security-dashboard/')
        assert response.status_code == 200

    def test_threat_analysis(self):
        SecurityEvent.objects.create(event_type="brute_force", severity="high", source_ip="1.1.1.1", description="Test")
        client = APIClient()
        response = client.get('/api/superadmin/admin/threat-analysis/')
        assert response.status_code == 200
