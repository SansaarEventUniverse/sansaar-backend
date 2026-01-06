import pytest
from django.core.exceptions import ValidationError
from domain.models import Connection

@pytest.mark.django_db
class TestConnection:
    def test_create_connection(self):
        connection = Connection.objects.create(from_user_id=1, to_user_id=2)
        assert connection.from_user_id == 1
        assert connection.to_user_id == 2
        assert connection.status == 'pending'
    
    def test_connection_is_pending(self):
        connection = Connection.objects.create(from_user_id=1, to_user_id=2)
        assert connection.is_pending() is True
    
    def test_connection_accept(self):
        connection = Connection.objects.create(from_user_id=1, to_user_id=2)
        connection.accept()
        assert connection.is_accepted() is True
        assert connection.status == 'accepted'
    
    def test_connection_reject(self):
        connection = Connection.objects.create(from_user_id=1, to_user_id=2)
        connection.reject()
        assert connection.status == 'rejected'
    
    def test_cannot_connect_to_self(self):
        connection = Connection(from_user_id=1, to_user_id=1)
        with pytest.raises(ValidationError):
            connection.clean()
    
    def test_unique_connection(self):
        Connection.objects.create(from_user_id=1, to_user_id=2)
        with pytest.raises(Exception):
            Connection.objects.create(from_user_id=1, to_user_id=2)
