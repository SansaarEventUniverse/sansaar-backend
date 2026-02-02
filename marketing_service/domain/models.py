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

class SMSTemplate(models.Model):
    name = models.CharField(max_length=200)
    message = models.TextField(max_length=160)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def render(self, context):
        message = self.message
        for key, value in context.items():
            message = message.replace(f'{{{{{key}}}}}', str(value))
        return message

    def __str__(self):
        return self.name

class SMSCampaign(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    ]

    name = models.CharField(max_length=200)
    message = models.TextField(max_length=160)
    template = models.ForeignKey(SMSTemplate, on_delete=models.SET_NULL, null=True, blank=True)
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

class AutomationWorkflow(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
    ]

    name = models.CharField(max_length=200)
    trigger_type = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def activate(self):
        self.status = 'active'
        self.save()

    def pause(self):
        self.status = 'paused'
        self.save()

    def complete(self):
        self.status = 'completed'
        self.save()

    def __str__(self):
        return self.name

class WorkflowTrigger(models.Model):
    workflow = models.ForeignKey(AutomationWorkflow, on_delete=models.CASCADE, related_name='triggers')
    trigger_type = models.CharField(max_length=100)
    conditions = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return True

    def __str__(self):
        return f"{self.workflow.name} - {self.trigger_type}"

class AudienceSegment(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('archived', 'Archived'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def activate(self):
        self.status = 'active'
        self.save()

    def archive(self):
        self.status = 'archived'
        self.save()

    def __str__(self):
        return self.name

class SegmentRule(models.Model):
    segment = models.ForeignKey(AudienceSegment, on_delete=models.CASCADE, related_name='rules')
    field = models.CharField(max_length=100)
    operator = models.CharField(max_length=50)
    value = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return True

    def __str__(self):
        return f"{self.segment.name} - {self.field} {self.operator} {self.value}"

class ABTest(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('paused', 'Paused'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def start(self):
        self.status = 'running'
        self.save()

    def complete(self):
        self.status = 'completed'
        self.save()

    def pause(self):
        self.status = 'paused'
        self.save()

    def __str__(self):
        return self.name

class TestVariant(models.Model):
    ab_test = models.ForeignKey(ABTest, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField(max_length=200)
    description = models.TextField()
    traffic_percentage = models.IntegerField(default=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return True

    def __str__(self):
        return f"{self.ab_test.name} - {self.name}"

class SocialPlatform(models.Model):
    name = models.CharField(max_length=100)
    platform_type = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return True

    def __str__(self):
        return self.name

class SocialMediaPost(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('published', 'Published'),
        ('failed', 'Failed'),
    ]

    content = models.TextField()
    platform = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    scheduled_at = models.DateTimeField(null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def publish(self):
        from django.utils import timezone
        self.status = 'published'
        self.published_at = timezone.now()
        self.save()

    def mark_failed(self):
        self.status = 'failed'
        self.save()

    def __str__(self):
        return f"{self.platform} - {self.content[:50]}"

class PersonalizationRule(models.Model):
    name = models.CharField(max_length=200)
    rule_type = models.CharField(max_length=50)
    conditions = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def activate(self):
        self.is_active = True
        self.save()

    def deactivate(self):
        self.is_active = False
        self.save()

    def __str__(self):
        return self.name

class UserPreference(models.Model):
    user_id = models.IntegerField()
    preference_type = models.CharField(max_length=100)
    preference_data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_valid(self):
        return True

    def __str__(self):
        return f"User {self.user_id} - {self.preference_type}"

class CampaignAnalytics(models.Model):
    campaign_id = models.IntegerField()
    campaign_type = models.CharField(max_length=50)
    total_sent = models.IntegerField(default=0)
    total_delivered = models.IntegerField(default=0)
    total_opened = models.IntegerField(default=0)
    total_clicked = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_open_rate(self):
        if self.total_delivered == 0:
            return 0.0
        return (self.total_opened / self.total_delivered) * 100

    def calculate_click_rate(self):
        if self.total_delivered == 0:
            return 0.0
        return (self.total_clicked / self.total_delivered) * 100

    def __str__(self):
        return f"Analytics for Campaign {self.campaign_id}"

class PerformanceMetric(models.Model):
    campaign_id = models.IntegerField()
    metric_name = models.CharField(max_length=100)
    metric_value = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return True

    def __str__(self):
        return f"{self.metric_name}: {self.metric_value}"

class MarketingIntelligence(models.Model):
    campaign_id = models.IntegerField()
    intelligence_type = models.CharField(max_length=100)
    data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def generate_insights(self):
        return {"insights": "generated"}

    def __str__(self):
        return f"Intelligence for Campaign {self.campaign_id}"

class IntelligenceInsight(models.Model):
    campaign_id = models.IntegerField()
    insight_type = models.CharField(max_length=100)
    insight_data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return True

    def __str__(self):
        return f"{self.insight_type} for Campaign {self.campaign_id}"
