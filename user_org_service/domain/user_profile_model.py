from django.core.validators import MaxLengthValidator
from django.db import models


class UserProfile(models.Model):
    user_id = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    bio = models.TextField(blank=True, null=True, validators=[MaxLengthValidator(500)])
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture_url = models.URLField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_profiles"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def update_info(self, first_name=None, last_name=None, bio=None):
        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
        if bio is not None:
            self.bio = bio
        self.full_clean()
        self.save()

    def update_profile_picture(self, url):
        self.profile_picture_url = url
        self.save()

    def delete_phone(self):
        self.phone = None
        self.save()

    def delete_address(self):
        self.address = None
        self.save()

    def delete_profile_picture(self):
        self.profile_picture_url = None
        self.save()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
