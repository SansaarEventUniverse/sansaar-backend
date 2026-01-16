from django.db import models
from django.core.exceptions import ValidationError

class Forum(models.Model):
    CATEGORY_CHOICES = [
        ('general', 'General'),
        ('technology', 'Technology'),
        ('community', 'Community'),
        ('news', 'News'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def deactivate(self):
        self.is_active = False
        self.save()
    
    def __str__(self):
        return self.title

class ForumPost(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('moderated', 'Moderated'),
        ('deleted', 'Deleted'),
    ]
    
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='posts')
    author_name = models.CharField(max_length=200)
    author_email = models.EmailField()
    title = models.CharField(max_length=300)
    content = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def is_published(self):
        return self.status == 'published'
    
    def moderate(self):
        self.status = 'moderated'
        self.save()
    
    def __str__(self):
        return self.title

class Feedback(models.Model):
    FEEDBACK_TYPE_CHOICES = [
        ('event', 'Event'),
        ('forum', 'Forum'),
        ('volunteer', 'Volunteer'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPE_CHOICES)
    entity_id = models.IntegerField()
    user_name = models.CharField(max_length=200)
    user_email = models.EmailField()
    rating = models.IntegerField()
    comment = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def is_positive(self):
        return self.rating >= 4
    
    def is_negative(self):
        return self.rating <= 2
    
    def approve(self):
        self.status = 'approved'
        self.save()
    
    def clean(self):
        if self.rating < 1 or self.rating > 5:
            raise ValidationError('Rating must be between 1 and 5')
    
    def __str__(self):
        return f"{self.feedback_type.title()} Feedback for {self.entity_id} - Rating: {self.rating}"
    
    class Meta:
        indexes = [
            models.Index(fields=['feedback_type', 'entity_id']),
            models.Index(fields=['status']),
        ]

class Connection(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    
    from_user_id = models.IntegerField()
    to_user_id = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def is_pending(self):
        return self.status == 'pending'
    
    def is_accepted(self):
        return self.status == 'accepted'
    
    def accept(self):
        self.status = 'accepted'
        self.save()
    
    def reject(self):
        self.status = 'rejected'
        self.save()
    
    def clean(self):
        if self.from_user_id == self.to_user_id:
            raise ValidationError('Cannot connect to yourself')
    
    def __str__(self):
        return f"Connection: {self.from_user_id} -> {self.to_user_id} ({self.status})"
    
    class Meta:
        unique_together = ['from_user_id', 'to_user_id']
        indexes = [
            models.Index(fields=['from_user_id', 'status']),
            models.Index(fields=['to_user_id', 'status']),
        ]

class InterestGroup(models.Model):
    CATEGORY_CHOICES = [
        ('technology', 'Technology'),
        ('sports', 'Sports'),
        ('arts', 'Arts'),
        ('education', 'Education'),
        ('business', 'Business'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    creator_user_id = models.IntegerField()
    is_active = models.BooleanField(default=True)
    max_members = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def is_full(self):
        if self.max_members == 0:
            return False
        return self.memberships.filter(status='active').count() >= self.max_members
    
    def deactivate(self):
        self.is_active = False
        self.save()
    
    def __str__(self):
        return self.name
    
    class Meta:
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['is_active']),
        ]

class GroupMembership(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('removed', 'Removed'),
    ]
    
    ROLE_CHOICES = [
        ('member', 'Member'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
    ]
    
    group = models.ForeignKey(InterestGroup, on_delete=models.CASCADE, related_name='memberships')
    user_id = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def is_active(self):
        return self.status == 'active'
    
    def activate(self):
        self.status = 'active'
        self.save()
    
    def remove(self):
        self.status = 'removed'
        self.save()
    
    def promote_to_moderator(self):
        self.role = 'moderator'
        self.save()
    
    def __str__(self):
        return f"{self.user_id} in {self.group.name} ({self.status})"
    
    class Meta:
        unique_together = ['group', 'user_id']
        indexes = [
            models.Index(fields=['user_id', 'status']),
            models.Index(fields=['group', 'status']),
        ]

class MentorshipProgram(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    skills_required = models.TextField()
    duration_weeks = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def is_active(self):
        return self.status == 'active'
    
    def complete(self):
        self.status = 'completed'
        self.save()
    
    def cancel(self):
        self.status = 'cancelled'
        self.save()
    
    def __str__(self):
        return self.title
    
    class Meta:
        indexes = [
            models.Index(fields=['status']),
        ]

class MentorMentee(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    program = models.ForeignKey(MentorshipProgram, on_delete=models.CASCADE, related_name='relationships')
    mentor_user_id = models.IntegerField()
    mentee_user_id = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def is_active(self):
        return self.status == 'active'
    
    def activate(self):
        self.status = 'active'
        self.save()
    
    def complete(self):
        self.status = 'completed'
        self.save()
    
    def clean(self):
        if self.mentor_user_id == self.mentee_user_id:
            raise ValidationError('Mentor and mentee cannot be the same person')
    
    def __str__(self):
        return f"Mentor {self.mentor_user_id} - Mentee {self.mentee_user_id} ({self.status})"
    
    class Meta:
        unique_together = ['program', 'mentor_user_id', 'mentee_user_id']
        indexes = [
            models.Index(fields=['mentor_user_id', 'status']),
            models.Index(fields=['mentee_user_id', 'status']),
        ]

class Achievement(models.Model):
    CATEGORY_CHOICES = [
        ('participation', 'Participation'),
        ('contribution', 'Contribution'),
        ('leadership', 'Leadership'),
        ('learning', 'Learning'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    points = models.IntegerField(default=0)
    badge_icon = models.CharField(max_length=100, blank=True)
    criteria = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['is_active']),
        ]

class UserAchievement(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name='user_achievements')
    user_id = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    progress = models.IntegerField(default=0)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def is_completed(self):
        return self.status == 'completed'
    
    def complete(self):
        from django.utils import timezone
        self.status = 'completed'
        self.progress = 100
        self.completed_at = timezone.now()
        self.save()
    
    def update_progress(self, progress):
        self.progress = min(progress, 100)
        if self.progress >= 100:
            self.complete()
        else:
            self.save()
    
    def __str__(self):
        return f"{self.user_id} - {self.achievement.name} ({self.progress}%)"
    
    class Meta:
        unique_together = ['achievement', 'user_id']
        indexes = [
            models.Index(fields=['user_id', 'status']),
        ]

class SharedContent(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('article', 'Article'),
        ('document', 'Document'),
        ('link', 'Link'),
        ('media', 'Media'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES)
    content_url = models.URLField(blank=True)
    creator_user_id = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_collaborative = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def is_published(self):
        return self.status == 'published'
    
    def publish(self):
        self.status = 'published'
        self.save()
    
    def archive(self):
        self.status = 'archived'
        self.save()
    
    def __str__(self):
        return self.title
    
    class Meta:
        indexes = [
            models.Index(fields=['creator_user_id']),
            models.Index(fields=['status']),
            models.Index(fields=['content_type']),
        ]

class ContentCollaboration(models.Model):
    ROLE_CHOICES = [
        ('viewer', 'Viewer'),
        ('editor', 'Editor'),
        ('owner', 'Owner'),
    ]
    
    content = models.ForeignKey(SharedContent, on_delete=models.CASCADE, related_name='collaborations')
    user_id = models.IntegerField()
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='viewer')
    joined_at = models.DateTimeField(auto_now_add=True)
    
    def is_editor(self):
        return self.role in ['editor', 'owner']
    
    def promote_to_editor(self):
        self.role = 'editor'
        self.save()
    
    def __str__(self):
        return f"{self.user_id} - {self.content.title} ({self.role})"
    
    class Meta:
        unique_together = ['content', 'user_id']
        indexes = [
            models.Index(fields=['user_id']),
            models.Index(fields=['content', 'role']),
        ]

class ModerationRule(models.Model):
    RULE_TYPE_CHOICES = [
        ('keyword', 'Keyword Filter'),
        ('spam', 'Spam Detection'),
        ('profanity', 'Profanity Filter'),
        ('harassment', 'Harassment Detection'),
    ]
    
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    name = models.CharField(max_length=200)
    rule_type = models.CharField(max_length=20, choices=RULE_TYPE_CHOICES)
    pattern = models.TextField()
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.severity})"
    
    class Meta:
        indexes = [
            models.Index(fields=['rule_type']),
            models.Index(fields=['is_active']),
        ]

class ModerationAction(models.Model):
    ACTION_TYPE_CHOICES = [
        ('warning', 'Warning'),
        ('remove', 'Remove Content'),
        ('suspend', 'Suspend User'),
        ('ban', 'Ban User'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    rule = models.ForeignKey(ModerationRule, on_delete=models.CASCADE, related_name='actions', null=True, blank=True)
    action_type = models.CharField(max_length=20, choices=ACTION_TYPE_CHOICES)
    target_type = models.CharField(max_length=50)
    target_id = models.IntegerField()
    moderator_id = models.IntegerField(null=True, blank=True)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def approve(self):
        self.status = 'approved'
        self.save()
    
    def reject(self):
        self.status = 'rejected'
        self.save()
    
    def __str__(self):
        return f"{self.action_type} on {self.target_type}:{self.target_id}"
    
    class Meta:
        indexes = [
            models.Index(fields=['target_type', 'target_id']),
            models.Index(fields=['status']),
        ]

from .resource_library import ResourceLibrary, SharedResource
