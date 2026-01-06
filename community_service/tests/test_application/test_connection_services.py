import pytest
from domain.models import Connection
from application.services.connection_service import ConnectionManagementService

@pytest.mark.django_db
class TestConnectionManagementService:
    def test_send_connection_request(self):
        service = ConnectionManagementService()
        connection = service.send_connection_request(1, 2)
        assert connection.from_user_id == 1
        assert connection.to_user_id == 2
        assert connection.is_pending()
    
    def test_accept_connection(self):
        connection = Connection.objects.create(from_user_id=1, to_user_id=2)
        service = ConnectionManagementService()
        updated = service.accept_connection(connection.id)
        assert updated.is_accepted()
    
    def test_reject_connection(self):
        connection = Connection.objects.create(from_user_id=1, to_user_id=2)
        service = ConnectionManagementService()
        updated = service.reject_connection(connection.id)
        assert updated.status == 'rejected'
    
    def test_get_user_connections(self):
        Connection.objects.create(from_user_id=1, to_user_id=2, status='accepted')
        Connection.objects.create(from_user_id=3, to_user_id=1, status='accepted')
        Connection.objects.create(from_user_id=1, to_user_id=4, status='pending')
        service = ConnectionManagementService()
        connections = service.get_user_connections(1)
        assert connections.count() == 2
    
    def test_get_pending_requests(self):
        Connection.objects.create(from_user_id=1, to_user_id=2, status='pending')
        Connection.objects.create(from_user_id=3, to_user_id=2, status='pending')
        Connection.objects.create(from_user_id=4, to_user_id=2, status='accepted')
        service = ConnectionManagementService()
        pending = service.get_pending_requests(2)
        assert pending.count() == 2
