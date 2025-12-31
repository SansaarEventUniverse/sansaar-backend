import pytest
from rest_framework.test import APIClient
from domain.models import SystemHealth, APIUsage, Notification, SecurityEvent


@pytest.mark.django_db
class TestSystemHealthE2E:
    def test_complete_health_monitoring_workflow(self):
        client = APIClient()
        
        # Create health data
        SystemHealth.objects.create(service_name="auth_service", status="healthy", cpu_usage=45.0, memory_usage=50.0)
        
        # Get system health
        response = client.get('/api/superadmin/admin/system-health/')
        assert response.status_code == 200
        assert len(response.data) == 1
        
        # Get monitoring dashboard
        response = client.get('/api/superadmin/admin/monitoring/')
        assert response.status_code == 200


@pytest.mark.django_db
class TestAPIAnalyticsE2E:
    def test_complete_api_analytics_workflow(self):
        client = APIClient()
        
        # Create API usage data
        APIUsage.objects.create(endpoint="/api/events/", method="GET", status_code=200, response_time=0.1)
        
        # Get API analytics
        response = client.get('/api/superadmin/admin/api-analytics/')
        assert response.status_code == 200
        
        # Get API usage report
        response = client.get('/api/superadmin/admin/api-usage/')
        assert response.status_code == 200


@pytest.mark.django_db
class TestNotificationE2E:
    def test_complete_notification_workflow(self):
        client = APIClient()
        
        # Create notification
        response = client.post('/api/superadmin/admin/notifications/create/', {
            'title': 'System Alert',
            'message': 'Test message',
            'notification_type': 'alert'
        }, format='json')
        assert response.status_code == 201
        
        # Get notifications
        response = client.get('/api/superadmin/admin/notifications/')
        assert response.status_code == 200
        assert len(response.data) == 1


@pytest.mark.django_db
class TestSecurityMonitoringE2E:
    def test_complete_security_monitoring_workflow(self):
        client = APIClient()
        
        # Create security event
        SecurityEvent.objects.create(
            event_type="attack",
            severity="critical",
            source_ip="1.1.1.1",
            description="Attack detected"
        )
        
        # Get security events
        response = client.get('/api/superadmin/admin/security-events/')
        assert response.status_code == 200
        assert len(response.data) == 1
        
        # Get security dashboard
        response = client.get('/api/superadmin/admin/security-dashboard/')
        assert response.status_code == 200
        assert response.data['critical_events'] == 1
        
        # Get threat analysis
        response = client.get('/api/superadmin/admin/threat-analysis/')
        assert response.status_code == 200
        assert len(response.data) == 1
