from django.db import models

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
