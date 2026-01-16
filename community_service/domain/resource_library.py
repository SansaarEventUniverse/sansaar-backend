from django.db import models

class ResourceLibrary(models.Model):
    CATEGORY_CHOICES = [
        ('document', 'Document'),
        ('template', 'Template'),
        ('guide', 'Guide'),
        ('tool', 'Tool'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    created_by = models.IntegerField()
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class SharedResource(models.Model):
    library = models.ForeignKey(ResourceLibrary, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file_url = models.URLField()
    file_type = models.CharField(max_length=50)
    file_size = models.IntegerField(default=0)
    tags = models.JSONField(default=list)
    download_count = models.IntegerField(default=0)
    uploaded_by = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def increment_download(self):
        self.download_count += 1
        self.save()

    def __str__(self):
        return self.title
