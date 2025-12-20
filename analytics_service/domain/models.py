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


class EventMetrics(models.Model):
    event_id = models.CharField(max_length=100)
    total_views = models.IntegerField(default=0)
    total_registrations = models.IntegerField(default=0)
    total_attendance = models.IntegerField(default=0)
    revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'event_metrics'
        indexes = [
            models.Index(fields=['event_id']),
        ]

    def clean(self):
        if not self.event_id:
            raise ValidationError({'event_id': 'Event ID is required'})

    def calculate_conversion_rate(self):
        if self.total_views > 0:
            return (self.total_registrations / self.total_views) * 100
        return 0.0

    def calculate_attendance_rate(self):
        if self.total_registrations > 0:
            return (self.total_attendance / self.total_registrations) * 100
        return 0.0

    @classmethod
    def get_metrics_by_event(cls, event_id):
        return cls.objects.filter(event_id=event_id).first()


class AttendanceAnalytics(models.Model):
    event_id = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100)
    check_in_time = models.DateTimeField()
    check_out_time = models.DateTimeField(null=True, blank=True)
    is_checked_in = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'attendance_analytics'
        indexes = [
            models.Index(fields=['event_id', 'user_id']),
        ]

    def clean(self):
        if not self.event_id:
            raise ValidationError({'event_id': 'Event ID is required'})

    def check_out(self, check_out_time):
        self.check_out_time = check_out_time
        self.is_checked_in = False
        self.save(update_fields=['check_out_time', 'is_checked_in'])

    @classmethod
    def get_event_attendance(cls, event_id):
        return cls.objects.filter(event_id=event_id)


class FinancialReport(models.Model):
    event_id = models.CharField(max_length=100)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_expenses = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    net_profit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'financial_reports'

    def clean(self):
        if not self.event_id:
            raise ValidationError({'event_id': 'Event ID is required'})

    def save(self, *args, **kwargs):
        self.net_profit = self.total_revenue - self.total_expenses
        super().save(*args, **kwargs)

    def calculate_profit_margin(self):
        if self.total_revenue > 0:
            return float((self.net_profit / self.total_revenue) * 100)
        return 0.0


class RevenueAnalytics(models.Model):
    event_id = models.CharField(max_length=100)
    ticket_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    sponsorship_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'revenue_analytics'

    def save(self, *args, **kwargs):
        self.total_revenue = self.ticket_revenue + self.sponsorship_revenue
        super().save(*args, **kwargs)

    def calculate_revenue_breakdown(self):
        if self.total_revenue > 0:
            return {
                'ticket_percentage': float((self.ticket_revenue / self.total_revenue) * 100),
                'sponsorship_percentage': float((self.sponsorship_revenue / self.total_revenue) * 100)
            }
        return {'ticket_percentage': 0.0, 'sponsorship_percentage': 0.0}


class UserAnalytics(models.Model):
    user_id = models.CharField(max_length=100)
    total_events_attended = models.IntegerField(default=0)
    total_tickets_purchased = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_analytics'

    def clean(self):
        if not self.user_id:
            raise ValidationError({'user_id': 'User ID is required'})

    def calculate_engagement_score(self):
        return self.total_events_attended + self.total_tickets_purchased


class UserActivity(models.Model):
    user_id = models.CharField(max_length=100)
    activity_type = models.CharField(max_length=50)
    event_id = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_activities'
        indexes = [
            models.Index(fields=['user_id', 'created_at']),
        ]

    @classmethod
    def get_user_activities(cls, user_id):
        return cls.objects.filter(user_id=user_id)


class Visualization(models.Model):
    name = models.CharField(max_length=200)
    visualization_type = models.CharField(max_length=50)
    config = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'visualizations'

    def get_chart_count(self):
        return self.charts.count()


class Chart(models.Model):
    visualization = models.ForeignKey(Visualization, on_delete=models.CASCADE, related_name='charts')
    chart_type = models.CharField(max_length=50)
    data = models.JSONField()
    config = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'charts'

    def validate_chart_data(self):
        return isinstance(self.data, dict)


class Visualization(models.Model):
    name = models.CharField(max_length=200)
    visualization_type = models.CharField(max_length=50)
    config = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'visualizations'

    def get_chart_count(self):
        return self.charts.count()


class Chart(models.Model):
    visualization = models.ForeignKey(Visualization, on_delete=models.CASCADE, related_name='charts')
    chart_type = models.CharField(max_length=50)
    data = models.JSONField()
    config = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'charts'

    def validate_chart_data(self):
        return isinstance(self.data, dict)


class CustomReport(models.Model):
    name = models.CharField(max_length=200)
    report_type = models.CharField(max_length=50)
    config = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'custom_reports'

    def get_metrics_count(self):
        return len(self.config.get('metrics', []))


class ReportTemplate(models.Model):
    name = models.CharField(max_length=200)
    template_type = models.CharField(max_length=50)
    template_config = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'report_templates'


class PerformanceMetric(models.Model):
    metric_name = models.CharField(max_length=100)
    metric_value = models.FloatField()
    metric_unit = models.CharField(max_length=50, default="")
    threshold = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'performance_metrics'

    def is_healthy(self):
        if self.threshold:
            return self.metric_value < self.threshold
        return True


class SystemHealth(models.Model):
    service_name = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    cpu_usage = models.FloatField(default=0.0)
    memory_usage = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'system_health'

    def is_critical(self):
        return self.status == "critical"


class DataExport(models.Model):
    export_name = models.CharField(max_length=200)
    export_format = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default="pending")
    file_path = models.CharField(max_length=500, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'data_exports'

    def is_completed(self):
        return self.status == "completed"


class ExportTemplate(models.Model):
    template_name = models.CharField(max_length=200)
    export_format = models.CharField(max_length=50)
    config = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'export_templates'


__all__ = ['AnalyticsEvent', 'MetricCalculation', 'Dashboard', 'DashboardWidget', 'EventMetrics', 'AttendanceAnalytics', 'FinancialReport', 'RevenueAnalytics', 'UserAnalytics', 'UserActivity', 'Visualization', 'Chart', 'CustomReport', 'ReportTemplate', 'PerformanceMetric', 'SystemHealth', 'DataExport', 'ExportTemplate']
