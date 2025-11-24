import uuid
from typing import List, Dict, Any
from django.db.models import Count, Avg, Q
from django.utils import timezone
from datetime import timedelta

from domain.fraud import FraudAlert, SecurityRule


class FraudRepository:
    """Repository for fraud data access."""
    
    def get_open_alerts(self) -> List[FraudAlert]:
        """Get all open fraud alerts."""
        return list(FraudAlert.objects.filter(status='open').order_by('-created_at'))
    
    def get_user_alerts(self, user_id: uuid.UUID) -> List[FraudAlert]:
        """Get alerts for a specific user."""
        return list(FraudAlert.objects.filter(user_id=user_id).order_by('-created_at'))
    
    def get_fraud_analytics(self) -> Dict[str, Any]:
        """Get fraud analytics."""
        alerts = FraudAlert.objects.all()
        
        stats = alerts.aggregate(
            total_alerts=Count('id'),
            avg_risk_score=Avg('risk_score'),
            open_alerts=Count('id', filter=Q(status='open')),
            high_risk_alerts=Count('id', filter=Q(severity__in=['high', 'critical']))
        )
        
        return {
            'total_alerts': stats['total_alerts'] or 0,
            'avg_risk_score': round(stats['avg_risk_score'] or 0, 2),
            'open_alerts': stats['open_alerts'] or 0,
            'high_risk_alerts': stats['high_risk_alerts'] or 0
        }


class FraudDetectionEngine:
    """Utility for fraud detection."""
    
    @staticmethod
    def calculate_risk_score(factors: Dict[str, int]) -> int:
        """Calculate risk score from factors."""
        total_score = sum(factors.values())
        return min(total_score, 100)
    
    @staticmethod
    def is_suspicious_pattern(order_count: int, time_window_hours: int = 24) -> bool:
        """Check for suspicious ordering patterns."""
        threshold = 5 if time_window_hours <= 24 else 10
        return order_count > threshold
