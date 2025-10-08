from django.db import models
from .custom_role_model import CustomRole


class UserCustomRole(models.Model):
    organization_id = models.CharField(max_length=255, db_index=True)
    user_id = models.CharField(max_length=255, db_index=True)
    custom_role = models.ForeignKey(CustomRole, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    assigned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_custom_roles'
        indexes = [
            models.Index(fields=['organization_id', 'user_id']),
            models.Index(fields=['user_id', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.user_id}:{self.custom_role.name}"
