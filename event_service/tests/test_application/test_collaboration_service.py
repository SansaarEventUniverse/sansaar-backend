import pytest
from domain.models import EventCollaboration, CollaborationTask
from application.collaboration_service import EventCollaborationService, TaskManagementService, TeamCoordinationService

@pytest.mark.django_db
class TestEventCollaborationService:
    def test_create_collaboration(self):
        """Test creating collaboration"""
        service = EventCollaborationService()
        collab = service.create_collaboration({
            'event_id': 1,
            'name': 'Planning',
            'created_by': 1
        })
        assert collab.name == 'Planning'

    def test_get_collaboration(self):
        """Test getting collaboration"""
        collab = EventCollaboration.objects.create(
            event_id=1,
            name='Planning',
            created_by=1
        )
        service = EventCollaborationService()
        result = service.get_collaboration(collab.id)
        assert result.id == collab.id

    def test_get_event_collaborations(self):
        """Test getting event collaborations"""
        EventCollaboration.objects.create(event_id=1, name='Planning', created_by=1)
        EventCollaboration.objects.create(event_id=1, name='Marketing', created_by=1)
        service = EventCollaborationService()
        collabs = service.get_event_collaborations(1)
        assert collabs.count() == 2

@pytest.mark.django_db
class TestTaskManagementService:
    def test_create_task(self):
        """Test creating task"""
        collab = EventCollaboration.objects.create(
            event_id=1,
            name='Planning',
            created_by=1
        )
        service = TaskManagementService()
        task = service.create_task({
            'collaboration': collab,
            'title': 'Setup venue'
        })
        assert task.title == 'Setup venue'

    def test_get_tasks(self):
        """Test getting tasks"""
        collab = EventCollaboration.objects.create(
            event_id=1,
            name='Planning',
            created_by=1
        )
        CollaborationTask.objects.create(collaboration=collab, title='Task 1')
        CollaborationTask.objects.create(collaboration=collab, title='Task 2')
        service = TaskManagementService()
        tasks = service.get_tasks(collab.id)
        assert tasks.count() == 2

    def test_update_task_status(self):
        """Test updating task status"""
        collab = EventCollaboration.objects.create(
            event_id=1,
            name='Planning',
            created_by=1
        )
        task = CollaborationTask.objects.create(
            collaboration=collab,
            title='Setup venue'
        )
        service = TaskManagementService()
        updated = service.update_task_status(task.id, 'completed')
        assert updated.status == 'completed'

@pytest.mark.django_db
class TestTeamCoordinationService:
    def test_add_team_member(self):
        """Test adding team member"""
        collab = EventCollaboration.objects.create(
            event_id=1,
            name='Planning',
            created_by=1
        )
        service = TeamCoordinationService()
        result = service.add_team_member(collab.id, 2)
        assert 2 in result.team_members

    def test_remove_team_member(self):
        """Test removing team member"""
        collab = EventCollaboration.objects.create(
            event_id=1,
            name='Planning',
            created_by=1,
            team_members=[2, 3]
        )
        service = TeamCoordinationService()
        result = service.remove_team_member(collab.id, 2)
        assert 2 not in result.team_members

    def test_get_team_members(self):
        """Test getting team members"""
        collab = EventCollaboration.objects.create(
            event_id=1,
            name='Planning',
            created_by=1,
            team_members=[2, 3, 4]
        )
        service = TeamCoordinationService()
        members = service.get_team_members(collab.id)
        assert len(members) == 3
