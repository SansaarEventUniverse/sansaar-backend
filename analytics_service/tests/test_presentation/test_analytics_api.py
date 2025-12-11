import pytest
from rest_framework.test import APIClient
from domain.models import AnalyticsEvent


@pytest.mark.django_db
class TestAnalyticsAPI:
    def setup_method(self):
        self.client = APIClient()

    def test_get_analytics(self):
        AnalyticsEvent.objects.create(event_type='page_view', event_data={})
        AnalyticsEvent.objects.create(event_type='click', event_data={})
        response = self.client.get('/api/analytics/')
        assert response.status_code == 200
        assert 'total_events' in response.data
        assert response.data['total_events'] == 2

    def test_get_realtime_metrics(self):
        AnalyticsEvent.objects.create(event_type='page_view', event_data={})
        response = self.client.get('/api/analytics/real-time/')
        assert response.status_code == 200
        assert 'total_events' in response.data
        assert response.data['total_events'] >= 1

    def test_analytics_query_by_event_type(self):
        AnalyticsEvent.objects.create(event_type='page_view', event_data={})
        AnalyticsEvent.objects.create(event_type='page_view', event_data={})
        AnalyticsEvent.objects.create(event_type='click', event_data={})
        response = self.client.post('/api/analytics/query/', {'event_type': 'page_view'}, format='json')
        assert response.status_code == 200
        assert response.data['count'] == 2

    def test_analytics_query_by_user(self):
        AnalyticsEvent.objects.create(event_type='view', event_data={}, user_id='123')
        AnalyticsEvent.objects.create(event_type='click', event_data={}, user_id='123')
        response = self.client.post('/api/analytics/query/', {'user_id': '123'}, format='json')
        assert response.status_code == 200
        assert response.data['count'] == 2

    def test_create_analytics_event_valid(self):
        event_data = {'event_type': 'page_view', 'event_data': {'page': '/home'}, 'user_id': '123'}
        response = self.client.post('/api/analytics/events/', event_data, format='json')
        assert response.status_code == 201
        assert response.data['event_type'] == 'page_view'
        assert 'id' in response.data

    def test_create_analytics_event_missing_event_type(self):
        event_data = {'event_data': {'page': '/home'}}
        response = self.client.post('/api/analytics/events/', event_data, format='json')
        assert response.status_code == 400
        assert 'event_type' in response.data

    def test_create_analytics_event_missing_event_data(self):
        event_data = {'event_type': 'page_view'}
        response = self.client.post('/api/analytics/events/', event_data, format='json')
        assert response.status_code == 400
        assert 'event_data' in response.data

    def test_analytics_query_invalid_date(self):
        response = self.client.post('/api/analytics/query/', {'start_date': 'invalid'}, format='json')
        assert response.status_code == 400
        assert 'start_date' in response.data
