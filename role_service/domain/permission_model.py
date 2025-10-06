from django.db import models


class Permission(models.Model):
    ROLE_CHOICES = [
        ('ORGANIZATION', 'Organization'),
        ('ORGANIZER', 'Organizer'),
        ('VOLUNTEER', 'Volunteer'),
        ('ATTENDEE', 'Attendee'),
    ]
    
    RESOURCE_CHOICES = [
        ('EVENT', 'Event'),
        ('TICKET', 'Ticket'),
        ('ATTENDEE', 'Attendee'),
        ('SCHEDULE', 'Schedule'),
    ]
    
    ACTION_CHOICES = [
        ('CREATE', 'Create'),
        ('READ', 'Read'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
    ]
    
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    resource = models.CharField(max_length=50, choices=RESOURCE_CHOICES)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    
    class Meta:
        db_table = 'permissions'
        unique_together = [['role', 'resource', 'action']]
        indexes = [
            models.Index(fields=['role', 'resource']),
        ]
    
    def __str__(self):
        return f"{self.role}:{self.resource}:{self.action}"
