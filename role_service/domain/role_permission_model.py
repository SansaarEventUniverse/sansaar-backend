from django.db import models
from .custom_role_model import CustomRole


class RolePermission(models.Model):
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
    
    custom_role = models.ForeignKey(CustomRole, on_delete=models.CASCADE, related_name='permissions')
    resource = models.CharField(max_length=50, choices=RESOURCE_CHOICES)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    
    class Meta:
        db_table = 'role_permissions'
        unique_together = [['custom_role', 'resource', 'action']]
        indexes = [
            models.Index(fields=['custom_role', 'resource']),
        ]
    
    def __str__(self):
        return f"{self.custom_role}:{self.resource}:{self.action}"
