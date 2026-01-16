import pytest
from django.utils import timezone
from datetime import timedelta
from domain.models import EventCollaboration, CollaborationTask
from infrastructure.repositories.collaboration_repository import CollaborationRepository

@pytest.mark.django_db
class TestCollaborationRepository:
    def test_get_collaboration_stats(self):
        """Test getting collaboration statistics"""
        collab = EventCollaboration.objects.create(
            event_id=1,
            name='Planning',
            created_by=1,
            team_members=[2, 3]
        )
        CollaborationTask.objects.create(collaboration=collab, title='Task 1', status='completed')
        CollaborationTask.objects.create(collaboration=collab, title='Task 2', status='in_progress')
        CollaborationTask.objects.create(collaboration=collab, title='Task 3', status='pending')
        
        repo = CollaborationRepository()
        stats = repo.get_collaboration_stats(collab.id)
        
        assert stats['total_tasks'] == 3
        assert stats['completed'] == 1
        assert stats['in_progress'] == 1
        assert stats['pending'] == 1
        assert stats['team_size'] == 2

    def test_get_user_tasks(self):
        """Test getting user tasks"""
        collab = EventCollaboration.objects.create(
            event_id=1,
            name='Planning',
            created_by=1,
            team_members=[2]
        )
        CollaborationTask.objects.create(collaboration=collab, title='Task 1', assigned_to=2)
        CollaborationTask.objects.create(collaboration=collab, title='Task 2', assigned_to=2)
        CollaborationTask.objects.create(collaboration=collab, title='Task 3', assigned_to=3)
        
        repo = CollaborationRepository()
        tasks = repo.get_user_tasks(2)
        assert tasks.count() == 2

    def test_get_overdue_tasks(self):
        """Test getting overdue tasks"""
        collab = EventCollaboration.objects.create(
            event_id=1,
            name='Planning',
            created_by=1
        )
        past_date = timezone.now() - timedelta(days=1)
        future_date = timezone.now() + timedelta(days=1)
        
        CollaborationTask.objects.create(
            collaboration=collab,
            title='Overdue',
            due_date=past_date,
            status='pending'
        )
        CollaborationTask.objects.create(
            collaboration=collab,
            title='Not overdue',
            due_date=future_date,
            status='pending'
        )
        
        repo = CollaborationRepository()
        overdue = repo.get_overdue_tasks()
        assert overdue.count() == 1
