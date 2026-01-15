from domain.models import EventCollaboration, CollaborationTask

class EventCollaborationService:
    def create_collaboration(self, data):
        return EventCollaboration.objects.create(**data)

    def get_collaboration(self, collaboration_id):
        return EventCollaboration.objects.get(id=collaboration_id)

    def get_event_collaborations(self, event_id):
        return EventCollaboration.objects.filter(event_id=event_id)

class TaskManagementService:
    def create_task(self, data):
        return CollaborationTask.objects.create(**data)

    def get_tasks(self, collaboration_id):
        return CollaborationTask.objects.filter(collaboration_id=collaboration_id)

    def update_task_status(self, task_id, status):
        task = CollaborationTask.objects.get(id=task_id)
        task.status = status
        task.save()
        return task

class TeamCoordinationService:
    def add_team_member(self, collaboration_id, user_id):
        collab = EventCollaboration.objects.get(id=collaboration_id)
        collab.add_member(user_id)
        return collab

    def remove_team_member(self, collaboration_id, user_id):
        collab = EventCollaboration.objects.get(id=collaboration_id)
        collab.remove_member(user_id)
        return collab

    def get_team_members(self, collaboration_id):
        collab = EventCollaboration.objects.get(id=collaboration_id)
        return collab.team_members
