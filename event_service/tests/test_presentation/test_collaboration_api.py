import pytest
from rest_framework.test import APIClient
from domain.models import EventCollaboration, CollaborationTask

@pytest.mark.django_db
class TestCollaborationAPI:
    def setup_method(self):
        self.client = APIClient()

    def test_create_collaboration(self):
        """Test creating collaboration"""
        response = self.client.post('/api/events/1/collaboration/', {
            'name': 'Event Planning',
            'description': 'Collaborate on planning',
            'created_by': 1
        }, format='json')
        assert response.status_code == 201
        assert response.data['name'] == 'Event Planning'
        assert response.data['event_id'] == 1

    def test_get_collaboration_tasks(self):
        """Test getting collaboration tasks"""
        collab = EventCollaboration.objects.create(
            event_id=1,
            name='Planning',
            created_by=1
        )
        CollaborationTask.objects.create(
            collaboration=collab,
            title='Setup venue'
        )
        CollaborationTask.objects.create(
            collaboration=collab,
            title='Send invites'
        )
        
        response = self.client.get(f'/api/events/collaborations/{collab.id}/tasks/')
        assert response.status_code == 200
        assert len(response.data) == 2

    def test_get_team_coordination(self):
        """Test getting team coordination"""
        collab = EventCollaboration.objects.create(
            event_id=1,
            name='Planning',
            created_by=1,
            team_members=[2, 3]
        )
        CollaborationTask.objects.create(
            collaboration=collab,
            title='Task 1',
            status='completed'
        )
        CollaborationTask.objects.create(
            collaboration=collab,
            title='Task 2',
            status='pending'
        )
        
        response = self.client.get(f'/api/events/collaborations/{collab.id}/team/')
        assert response.status_code == 200
        assert 'stats' in response.data
        assert 'team_members' in response.data
        assert response.data['stats']['total_tasks'] == 2
        assert response.data['stats']['team_size'] == 2
