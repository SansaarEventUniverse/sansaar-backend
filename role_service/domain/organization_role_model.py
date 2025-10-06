from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class OrganizationRole(models.Model):
    ROLE_CHOICES = [
        ('OWNER', 'Owner'),
        ('ADMIN', 'Admin'),
        ('MEMBER', 'Member'),
    ]
    
    organization_id = models.CharField(max_length=255, db_index=True)
    user_id = models.CharField(max_length=255, db_index=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    assigned_at = models.DateTimeField(auto_now_add=True)
    revoked_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'organization_roles'
        indexes = [
            models.Index(fields=['organization_id', 'user_id']),
            models.Index(fields=['user_id', 'is_active']),
            models.Index(fields=['organization_id', 'role', 'is_active']),
        ]
    
    def revoke(self):
        self.is_active = False
        self.revoked_at = timezone.now()
        self.save()
    
    def validate_ownership_transfer(self, new_owner_id):
        if self.role != 'OWNER':
            raise ValidationError('Only owners can transfer ownership')
        if not self.is_active:
            raise ValidationError('Cannot transfer from inactive owner')
        if self.user_id == new_owner_id:
            raise ValidationError('Cannot transfer ownership to self')
    
    @classmethod
    def get_active_owner(cls, organization_id):
        return cls.objects.filter(
            organization_id=organization_id,
            role='OWNER',
            is_active=True
        ).first()
