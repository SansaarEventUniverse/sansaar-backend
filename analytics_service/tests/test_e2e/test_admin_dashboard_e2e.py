import pytest
from rest_framework.test import APIClient
from domain.models import EventMetrics, FinancialReport, UserAnalytics, Dashboard


@pytest.mark.django_db
class TestEventAnalyticsE2E:
    def test_complete_event_analytics_workflow(self):
        """Test complete event analytics workflow from tracking to metrics"""
        client = APIClient()
        event_id = "event-e2e-123"
        
        # Create metrics first
        EventMetrics.objects.create(
            event_id=event_id,
            total_views=1,
            total_registrations=1
        )
        
        # Get metrics
        response = client.get(f'/api/analytics/events/{event_id}/metrics/')
        assert response.status_code == 200
        assert response.data['total_views'] == 1
        
        # Export metrics
        response = client.get(f'/api/analytics/events/{event_id}/export/')
        assert response.status_code == 200


@pytest.mark.django_db
class TestFinancialReportingE2E:
    def test_complete_financial_workflow(self):
        """Test complete financial reporting workflow"""
        client = APIClient()
        event_id = "event-fin-456"
        
        # Create financial report
        FinancialReport.objects.create(
            event_id=event_id,
            total_revenue=10000.00,
            total_expenses=3000.00,
            net_profit=7000.00
        )
        
        # Get financial report
        response = client.get(f'/api/analytics/events/{event_id}/financial/')
        assert response.status_code == 200
        assert float(response.data['total_revenue']) == 10000.00
        
        # Export financial data
        response = client.get(f'/api/analytics/events/{event_id}/financial/export/')
        assert response.status_code == 200


@pytest.mark.django_db
class TestUserManagementE2E:
    def test_complete_user_management_workflow(self):
        """Test complete user management workflow"""
        client = APIClient()
        
        # Create user analytics
        UserAnalytics.objects.create(
            user_id="user-e2e-789",
            total_events_attended=5,
            total_tickets_purchased=10
        )
        
        # Get all users
        response = client.get('/api/analytics/admin/users/')
        assert response.status_code == 200
        assert len(response.data) == 1
        
        # Get specific user analytics
        response = client.get('/api/analytics/admin/user-analytics/?user_id=user-e2e-789')
        assert response.status_code == 200
        assert response.data['engagement_score'] == 15
        
        # Get user activity
        response = client.get('/api/analytics/admin/user-activity/?user_id=user-e2e-789')
        assert response.status_code == 200


@pytest.mark.django_db
class TestDashboardE2E:
    def test_dashboard_creation_and_retrieval(self):
        """Test dashboard creation and retrieval workflow"""
        # Create dashboard directly
        dashboard = Dashboard.objects.create(
            organizer_id='org-123',
            name='Test Dashboard'
        )
        
        client = APIClient()
        
        # Get dashboard
        response = client.get(f'/api/analytics/organizer/dashboard/{dashboard.id}/')
        assert response.status_code == 200
        assert response.data['name'] == 'Test Dashboard'
