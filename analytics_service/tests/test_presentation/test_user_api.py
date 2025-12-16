import pytest
from rest_framework.test import APIClient
from domain.models import UserAnalytics, UserActivity


@pytest.mark.django_db
class TestUserManagementAPI:
    def test_get_user_analytics(self):
        UserAnalytics.objects.create(
            user_id="user-123",
            total_events_attended=5,
            total_tickets_purchased=10
        )
        client = APIClient()
        response = client.get('/api/analytics/admin/user-analytics/', {'user_id': 'user-123'})
        assert response.status_code == 200
        assert response.data['user_id'] == 'user-123'

    def test_get_user_activity(self):
        UserActivity.objects.create(user_id="user-123", activity_type="event_view")
        client = APIClient()
        response = client.get('/api/analytics/admin/user-activity/', {'user_id': 'user-123'})
        assert response.status_code == 200
        assert len(response.data) == 1

    def test_get_all_users(self):
        UserAnalytics.objects.create(user_id="user-1", total_events_attended=5)
        UserAnalytics.objects.create(user_id="user-2", total_events_attended=3)
        client = APIClient()
        response = client.get('/api/analytics/admin/users/')
        assert response.status_code == 200
        assert len(response.data) == 2
