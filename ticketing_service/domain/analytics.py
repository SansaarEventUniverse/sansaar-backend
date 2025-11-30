import uuid
from decimal import Decimal
from django.db import models
from django.utils import timezone


class TicketAnalytics(models.Model):
    """Analytics model for ticket sales."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_id = models.UUIDField(db_index=True)
    total_tickets = models.IntegerField(default=0)
    sold_tickets = models.IntegerField(default=0)
    revenue = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'ticket_analytics'
        indexes = [
            models.Index(fields=['event_id']),
        ]
    
    def __str__(self):
        return f"Analytics for Event {self.event_id}"
    
    def calculate_sold_percentage(self) -> float:
        """Calculate percentage of tickets sold."""
        if self.total_tickets == 0:
            return 0.0
        return (self.sold_tickets / self.total_tickets) * 100
    
    def calculate_average_ticket_price(self) -> Decimal:
        """Calculate average ticket price."""
        if self.sold_tickets == 0:
            return Decimal("0.00")
        return self.revenue / self.sold_tickets
    
    def is_sold_out(self) -> bool:
        """Check if event is sold out."""
        return self.sold_tickets >= self.total_tickets


class SalesMetrics(models.Model):
    """Sales metrics model for business intelligence."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_id = models.UUIDField(db_index=True)
    period_start = models.DateTimeField()
    period_end = models.DateTimeField()
    total_sales = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    transaction_count = models.IntegerField(default=0)
    previous_period_sales = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'sales_metrics'
        indexes = [
            models.Index(fields=['event_id', 'period_start']),
        ]
    
    def __str__(self):
        return f"Sales Metrics for Event {self.event_id}"
    
    def calculate_average_transaction_value(self) -> Decimal:
        """Calculate average transaction value."""
        if self.transaction_count == 0:
            return Decimal("0.00")
        return self.total_sales / self.transaction_count
    
    def calculate_daily_average(self) -> Decimal:
        """Calculate daily average sales."""
        days = (self.period_end - self.period_start).days
        if days == 0:
            return self.total_sales
        return self.total_sales / days
    
    def get_growth_rate(self) -> float:
        """Calculate growth rate compared to previous period."""
        if self.previous_period_sales == 0:
            return 0.0
        growth = ((self.total_sales - self.previous_period_sales) / self.previous_period_sales) * 100
        return float(growth)
