from django.db import models
from django.core.exceptions import ValidationError

class EventCollaboration(models.Model):
    event_id = models.IntegerField()
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    team_members = models.JSONField(default=list)
    created_by = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def add_member(self, user_id):
        if user_id not in self.team_members:
            self.team_members.append(user_id)
            self.save()

    def remove_member(self, user_id):
        if user_id in self.team_members:
            self.team_members.remove(user_id)
            self.save()

    def __str__(self):
        return f"{self.name} - Event {self.event_id}"

class CollaborationTask(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    collaboration = models.ForeignKey(EventCollaboration, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    assigned_to = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    due_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def assign(self, user_id):
        if user_id not in self.collaboration.team_members:
            raise ValidationError("User must be a team member")
        self.assigned_to = user_id
        self.save()

    def mark_completed(self):
        self.status = 'completed'
        self.save()

    def __str__(self):
        return f"{self.title} - {self.status}"
