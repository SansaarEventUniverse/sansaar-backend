from django.db import models


class CustomRole(models.Model):
    organization_id = models.CharField(max_length=255, db_index=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'custom_roles'
        unique_together = [['organization_id', 'name']]
        indexes = [
            models.Index(fields=['organization_id']),
        ]
    
    def __str__(self):
        return f"{self.organization_id}:{self.name}"
