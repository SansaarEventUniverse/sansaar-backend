from django.db import models
from django.utils import timezone

class CommunityAnalytics(models.Model):
    METRIC_TYPE_CHOICES = [
        ('user_growth', 'User Growth'),
        ('engagement', 'Engagement'),
        ('content', 'Content'),
        ('activity', 'Activity'),
    ]
    
    metric_type = models.CharField(max_length=20, choices=METRIC_TYPE_CHOICES)
    metric_value = models.FloatField()
    period_start = models.DateTimeField()
    period_end = models.DateTimeField()
    metadata = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_growth_rate(self, previous_value):
        if previous_value == 0:
            return 0
        return ((self.metric_value - previous_value) / previous_value) * 100

    def __str__(self):
        return f"{self.metric_type} - {self.metric_value}"

class EngagementMetrics(models.Model):
    user_id = models.IntegerField()
    posts_created = models.IntegerField(default=0)
    comments_made = models.IntegerField(default=0)
    likes_given = models.IntegerField(default=0)
    shares_made = models.IntegerField(default=0)
    engagement_score = models.FloatField(default=0.0)
    last_active = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_engagement_score(self):
        self.engagement_score = (
            self.posts_created * 5 +
            self.comments_made * 3 +
            self.likes_given * 1 +
            self.shares_made * 4
        )
        self.save()
        return self.engagement_score

    def __str__(self):
        return f"User {self.user_id} - Score: {self.engagement_score}"
