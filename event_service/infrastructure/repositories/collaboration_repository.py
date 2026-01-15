from domain.models import EventCollaboration, CollaborationTask
from django.db.models import Count, Q

class CollaborationRepository:
    def get_collaboration_stats(self, collaboration_id):
        collab = EventCollaboration.objects.get(id=collaboration_id)
        tasks = CollaborationTask.objects.filter(collaboration=collab)
        
        return {
            'total_tasks': tasks.count(),
            'completed': tasks.filter(status='completed').count(),
            'in_progress': tasks.filter(status='in_progress').count(),
            'pending': tasks.filter(status='pending').count(),
            'team_size': len(collab.team_members)
        }

    def get_user_tasks(self, user_id):
        return CollaborationTask.objects.filter(assigned_to=user_id)

    def get_overdue_tasks(self):
        from django.utils import timezone
        return CollaborationTask.objects.filter(
            due_date__lt=timezone.now(),
            status__in=['pending', 'in_progress']
        )
