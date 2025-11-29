from decimal import Decimal
from typing import Dict
from django.db.models import Count, Sum
from domain.subscription import Subscription


class SubscriptionAnalytics:
    """Analytics service for subscription metrics."""
    
    def get_active_subscriptions_count(self) -> int:
        """Get count of active subscriptions."""
        return Subscription.objects.filter(status='active').count()
    
    def get_monthly_recurring_revenue(self) -> Decimal:
        """Calculate monthly recurring revenue (MRR)."""
        subscriptions = Subscription.objects.filter(status='active')
        
        mrr = Decimal('0')
        for sub in subscriptions:
            if sub.billing_cycle == 'monthly':
                mrr += sub.amount
            elif sub.billing_cycle == 'quarterly':
                mrr += sub.amount / 3
            elif sub.billing_cycle == 'yearly':
                mrr += sub.amount / 12
        
        return mrr
    
    def get_churn_rate(self) -> float:
        """Calculate subscription churn rate."""
        total_count = Subscription.objects.count()
        if total_count == 0:
            return 0.0
        
        cancelled_count = Subscription.objects.filter(status='cancelled').count()
        return (cancelled_count / total_count) * 100
    
    def get_subscription_metrics(self) -> Dict:
        """Get comprehensive subscription metrics."""
        return {
            'active_count': self.get_active_subscriptions_count(),
            'mrr': self.get_monthly_recurring_revenue(),
            'churn_rate': self.get_churn_rate(),
            'total_count': Subscription.objects.count(),
            'paused_count': Subscription.objects.filter(status='paused').count(),
            'cancelled_count': Subscription.objects.filter(status='cancelled').count(),
        }
