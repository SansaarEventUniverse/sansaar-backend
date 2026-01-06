import pytest
from rest_framework.test import APIClient
from domain.models import Connection

@pytest.mark.django_db
class TestConnectionAPI:
    def test_connect_user(self):
        client = APIClient()
        data = {'from_user_id': 1, 'to_user_id': 2}
        response = client.post('/api/community/connections/connect/', data, format='json')
        assert response.status_code == 201
        assert response.data['from_user_id'] == 1
        assert response.data['to_user_id'] == 2
        assert response.data['status'] == 'pending'
    
    def test_get_connections(self):
        Connection.objects.create(from_user_id=1, to_user_id=2, status='accepted')
        Connection.objects.create(from_user_id=3, to_user_id=1, status='accepted')
        client = APIClient()
        response = client.get('/api/community/connections/?user_id=1')
        assert response.status_code == 200
        assert len(response.data['results']) == 2
    
    def test_update_connection_status_accept(self):
        connection = Connection.objects.create(from_user_id=1, to_user_id=2)
        client = APIClient()
        response = client.put(f'/api/community/connections/{connection.id}/status/', {'action': 'accept'}, format='json')
        assert response.status_code == 200
        assert response.data['status'] == 'accepted'
    
    def test_update_connection_status_reject(self):
        connection = Connection.objects.create(from_user_id=1, to_user_id=2)
        client = APIClient()
        response = client.put(f'/api/community/connections/{connection.id}/status/', {'action': 'reject'}, format='json')
        assert response.status_code == 200
        assert response.data['status'] == 'rejected'
    
    def test_get_recommendations(self):
        Connection.objects.create(from_user_id=1, to_user_id=2, status='accepted')
        Connection.objects.create(from_user_id=2, to_user_id=3, status='accepted')
        client = APIClient()
        response = client.get('/api/community/connections/recommendations/?user_id=1')
        assert response.status_code == 200
        assert 'recommendations' in response.data
