from django.db import models
from django.core.exceptions import ValidationError


class AnalyticsEvent(models.Model):
    event_type = models.CharField(max_length=100)
    event_data = models.JSONField()
    user_id = models.CharField(max_length=100, null=True, blank=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)
    is_processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'analytics_events'
        indexes = [
            models.Index(fields=['event_type', 'created_at']),
            models.Index(fields=['is_processed']),
        ]

    def clean(self):
        if not self.event_type:
            raise ValidationError({'event_type': 'Event type is required'})

    def mark_as_processed(self):
        from django.utils import timezone
        self.is_processed = True
        self.processed_at = timezone.now()
        self.save(update_fields=['is_processed', 'processed_at'])

    @classmethod
    def get_unprocessed_events(cls):
        return cls.objects.filter(is_processed=False).order_by('created_at')


class MetricCalculation(models.Model):
    metric_name = models.CharField(max_length=100)
    metric_value = models.FloatField()
    previous_value = models.FloatField(null=True, blank=True)
    calculation_type = models.CharField(max_length=50)
    time_period = models.CharField(max_length=50, null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'metric_calculations'
        indexes = [
            models.Index(fields=['metric_name', 'created_at']),
        ]

    def clean(self):
        if not self.metric_name:
            raise ValidationError({'metric_name': 'Metric name is required'})

    def calculate_percentage_change(self):
        if self.previous_value and self.previous_value != 0:
            return ((self.metric_value - self.previous_value) / self.previous_value) * 100
        return 0.0

    @classmethod
    def get_latest_metrics(cls):
        return cls.objects.order_by('-created_at')


class Dashboard(models.Model):
    organizer_id = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    layout = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'dashboards'
        indexes = [
            models.Index(fields=['organizer_id', 'is_active']),
        ]

    def clean(self):
        if not self.organizer_id:
            raise ValidationError({'organizer_id': 'Organizer ID is required'})

    def activate(self):
        self.is_active = True
        self.save(update_fields=['is_active'])

    def deactivate(self):
        self.is_active = False
        self.save(update_fields=['is_active'])

    @classmethod
    def get_active_dashboards(cls, organizer_id):
        return cls.objects.filter(organizer_id=organizer_id, is_active=True)


class DashboardWidget(models.Model):
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE, related_name='widgets')
    widget_type = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    config = models.JSONField(default=dict, blank=True)
    position = models.IntegerField(default=0)
    is_visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'dashboard_widgets'
        ordering = ['position']
        indexes = [
            models.Index(fields=['dashboard', 'position']),
        ]

    def clean(self):
        if not self.widget_type:
            raise ValidationError({'widget_type': 'Widget type is required'})

    def toggle_visibility(self):
        self.is_visible = not self.is_visible
        self.save(update_fields=['is_visible'])

    def update_position(self, new_position):
        self.position = new_position
        self.save(update_fields=['position'])

    @classmethod
    def get_visible_widgets(cls, dashboard):
        return cls.objects.filter(dashboard=dashboard, is_visible=True)


__all__ = ['AnalyticsEvent', 'MetricCalculation', 'Dashboard', 'DashboardWidget']

