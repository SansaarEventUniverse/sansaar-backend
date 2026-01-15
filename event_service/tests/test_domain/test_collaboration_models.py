import pytest
from django.core.exceptions import ValidationError
from domain.models import EventCollaboration, CollaborationTask

@pytest.mark.django_db
class TestEventCollaboration:
    def test_create_collaboration(self):
        """Test creating event collaboration"""
        collab = EventCollaboration.objects.create(
            event_id=1,
            name="Event Planning",
            description="Collaborate on event",
            created_by=1
        )
        assert collab.name == "Event Planning"
        assert collab.team_members == []

    def test_add_member(self):
        """Test adding team member"""
        collab = EventCollaboration.objects.create(
            event_id=1,
            name="Planning",
            created_by=1
        )
        collab.add_member(2)
        assert 2 in collab.team_members

    def test_remove_member(self):
        """Test removing team member"""
        collab = EventCollaboration.objects.create(
            event_id=1,
            name="Planning",
            created_by=1,
            team_members=[2, 3]
        )
        collab.remove_member(2)
        assert 2 not in collab.team_members
        assert 3 in collab.team_members

@pytest.mark.django_db
class TestCollaborationTask:
    def test_create_task(self):
        """Test creating collaboration task"""
        collab = EventCollaboration.objects.create(
            event_id=1,
            name="Planning",
            created_by=1
        )
        task = CollaborationTask.objects.create(
            collaboration=collab,
            title="Setup venue",
            priority='high'
        )
        assert task.title == "Setup venue"
        assert task.status == 'pending'
        assert task.priority == 'high'

    def test_assign_task(self):
        """Test assigning task to team member"""
        collab = EventCollaboration.objects.create(
            event_id=1,
            name="Planning",
            created_by=1,
            team_members=[2]
        )
        task = CollaborationTask.objects.create(
            collaboration=collab,
            title="Setup venue"
        )
        task.assign(2)
        assert task.assigned_to == 2

    def test_assign_task_non_member_fails(self):
        """Test assigning task to non-member fails"""
        collab = EventCollaboration.objects.create(
            event_id=1,
            name="Planning",
            created_by=1
        )
        task = CollaborationTask.objects.create(
            collaboration=collab,
            title="Setup venue"
        )
        with pytest.raises(ValidationError):
            task.assign(999)

    def test_mark_completed(self):
        """Test marking task as completed"""
        collab = EventCollaboration.objects.create(
            event_id=1,
            name="Planning",
            created_by=1
        )
        task = CollaborationTask.objects.create(
            collaboration=collab,
            title="Setup venue"
        )
        task.mark_completed()
        assert task.status == 'completed'
