from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class VolunteerOpportunity(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    volunteers_needed = models.IntegerField()
    volunteers_registered = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def is_active(self):
        return self.status == 'open' and not self.is_full()
    
    def is_full(self):
        return self.volunteers_registered >= self.volunteers_needed
    
    def clean(self):
        if self.end_date <= self.start_date:
            raise ValidationError('End date must be after start date')
    
    def __str__(self):
        return self.title

class VolunteerSkill(models.Model):
    PROFICIENCY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    opportunity = models.ForeignKey(VolunteerOpportunity, on_delete=models.CASCADE, related_name='skills')
    skill_name = models.CharField(max_length=100)
    proficiency_level = models.CharField(max_length=20, choices=PROFICIENCY_CHOICES)
    is_required = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.skill_name} ({self.proficiency_level})"
