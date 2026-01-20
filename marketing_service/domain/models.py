from django.db import models

class EmailTemplate(models.Model):
    name = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def render(self, context):
        content = self.content
        for key, value in context.items():
            content = content.replace(f'{{{{{key}}}}}', str(value))
        return content

    def __str__(self):
        return self.name

class EmailCampaign(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    ]

    name = models.CharField(max_length=200)
    subject = models.CharField(max_length=300)
    template = models.ForeignKey(EmailTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    scheduled_at = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def schedule(self):
        self.status = 'scheduled'
        self.save()

    def mark_sent(self):
        from django.utils import timezone
        self.status = 'sent'
        self.sent_at = timezone.now()
        self.save()

    def mark_failed(self):
        self.status = 'failed'
        self.save()

    def __str__(self):
        return self.name
