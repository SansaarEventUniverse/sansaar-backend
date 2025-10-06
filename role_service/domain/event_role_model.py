from django.db import models
from django.utils import timezone


class EventRole(models.Model):
    ROLE_CHOICES = [
        ('ORGANIZATION', 'Organization'),
        ('ORGANIZER', 'Organizer'),
        ('VOLUNTEER', 'Volunteer'),
        ('ATTENDEE', 'Attendee'),
    ]
    
    event_id = models.CharField(max_length=255, db_index=True)
    user_id = models.CharField(max_length=255, db_index=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    assigned_at = models.DateTimeField(auto_now_add=True)
    revoked_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'event_roles'
        unique_together = [['event_id', 'user_id', 'is_active']]
        indexes = [
            models.Index(fields=['event_id', 'user_id']),
            models.Index(fields=['user_id', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.user_id} - {self.role} - {self.event_id}"
    
    def revoke(self):
        self.is_active = False
        self.revoked_at = timezone.now()
        self.save()
