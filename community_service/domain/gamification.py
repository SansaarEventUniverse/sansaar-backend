from django.db import models

class GamificationRule(models.Model):
    RULE_TYPE_CHOICES = [
        ('post_created', 'Post Created'),
        ('comment_made', 'Comment Made'),
        ('like_received', 'Like Received'),
        ('share_made', 'Share Made'),
        ('daily_login', 'Daily Login'),
    ]
    
    name = models.CharField(max_length=200)
    rule_type = models.CharField(max_length=20, choices=RULE_TYPE_CHOICES)
    points = models.IntegerField()
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.points} points"

class UserReward(models.Model):
    REWARD_TYPE_CHOICES = [
        ('badge', 'Badge'),
        ('points', 'Points'),
        ('achievement', 'Achievement'),
    ]
    
    user_id = models.IntegerField()
    reward_type = models.CharField(max_length=20, choices=REWARD_TYPE_CHOICES)
    reward_name = models.CharField(max_length=200)
    points_earned = models.IntegerField(default=0)
    total_points = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    earned_at = models.DateTimeField(auto_now_add=True)

    def add_points(self, points):
        self.points_earned += points
        self.total_points += points
        self.level = self.total_points // 100 + 1
        self.save()

    def __str__(self):
        return f"User {self.user_id} - {self.reward_name}"
