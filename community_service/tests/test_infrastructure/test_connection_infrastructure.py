import pytest
from domain.models import Connection
from infrastructure.repositories.connection_repository import ConnectionRepository

@pytest.mark.django_db
class TestConnectionRepository:
    def test_get_mutual_connections(self):
        Connection.objects.create(from_user_id=1, to_user_id=3, status='accepted')
        Connection.objects.create(from_user_id=2, to_user_id=3, status='accepted')
        Connection.objects.create(from_user_id=1, to_user_id=4, status='accepted')
        
        repo = ConnectionRepository()
        mutual = repo.get_mutual_connections(1, 2)
        assert 3 in mutual
        assert len(mutual) == 1
    
    def test_get_connection_recommendations(self):
        Connection.objects.create(from_user_id=1, to_user_id=2, status='accepted')
        Connection.objects.create(from_user_id=2, to_user_id=3, status='accepted')
        Connection.objects.create(from_user_id=2, to_user_id=4, status='accepted')
        
        repo = ConnectionRepository()
        recommendations = repo.get_connection_recommendations(1, limit=5)
        assert 3 in recommendations or 4 in recommendations
