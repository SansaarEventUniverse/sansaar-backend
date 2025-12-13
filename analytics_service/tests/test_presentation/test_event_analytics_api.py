import pytest
from decimal import Decimal
from rest_framework.test import APIClient
from domain.models import EventMetrics, AttendanceAnalytics


@pytest.mark.django_db
class TestEventAnalyticsAPI:
    def test_track_view(self):
        client = APIClient()
        response = client.post('/api/analytics/events/event-123/track-view/')
        assert response.status_code == 200
        assert response.data['total_views'] == 1

    def test_track_registration(self):
        client = APIClient()
        response = client.post('/api/analytics/events/event-123/track-registration/')
        assert response.status_code == 200
        assert response.data['total_registrations'] == 1

    def test_get_metrics(self):
        EventMetrics.objects.create(
            event_id="event-123",
            total_views=100,
            total_registrations=50
        )
        client = APIClient()
        response = client.get('/api/analytics/events/event-123/metrics/')
        assert response.status_code == 200
        assert response.data['total_views'] == 100


@pytest.mark.django_db
class TestAttendanceAPI:
    def test_check_in(self):
        client = APIClient()
        response = client.post('/api/analytics/events/event-123/check-in/', {'user_id': 'user-456'}, format='json')
        assert response.status_code == 200
        assert response.data['is_checked_in'] is True

    def test_check_out(self):
        AttendanceAnalytics.objects.create(
            event_id="event-123",
            user_id="user-456",
            check_in_time="2024-01-01T10:00:00Z",
            is_checked_in=True
        )
        client = APIClient()
        response = client.post('/api/analytics/events/event-123/check-out/', {'user_id': 'user-456'}, format='json')
        assert response.status_code == 200
        assert response.data['is_checked_in'] is False


@pytest.mark.django_db
class TestMetricsExportAPI:
    def test_export_json(self):
        EventMetrics.objects.create(event_id="event123", total_views=100)
        client = APIClient()
        response = client.get('/api/analytics/events/event123/export/')
        assert response.status_code == 200

    def test_export_csv(self):
        EventMetrics.objects.create(event_id="event123", total_views=100)
        client = APIClient()
        response = client.get('/api/analytics/events/event123/export-csv/')
        assert response.status_code == 200
        assert 'text/csv' in response.get('Content-Type', '')
