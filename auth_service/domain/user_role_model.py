from django.db import models
from .user_model import User


class UserRole(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_role")
    role = models.CharField(max_length=50, default="USER")
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_roles"
