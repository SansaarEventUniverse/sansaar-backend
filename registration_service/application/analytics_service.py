from typing import Dict, Any
import uuid
from django.db.models import Count, Q

from domain.analytics import RegistrationAnalytics
from domain.registration import Registration
from domain.waitlist import Waitlist
from domain.group_registration import GroupRegistration
from domain.capacity_rule import CapacityRule


class GenerateAnalyticsService:
    """Service for generating analytics data."""
    
    def execute(self, event_id: uuid.UUID) -> RegistrationAnalytics:
        """Generate or update analytics for an event."""
        # Get or create analytics
        analytics, created = RegistrationAnalytics.objects.get_or_create(
            event_id=event_id
        )
        
        # Calculate registration metrics
        registrations = Registration.objects.filter(event_id=event_id)
        analytics.total_registrations = registrations.count()
        analytics.confirmed_registrations = registrations.filter(status='confirmed').count()
        analytics.cancelled_registrations = registrations.filter(status='cancelled').count()
        
        # Calculate waitlist metrics
        waitlist = Waitlist.objects.filter(event_id=event_id)
        analytics.total_waitlist = waitlist.count()
        analytics.promoted_from_waitlist = waitlist.filter(is_promoted=True).count()
        
        # Calculate group metrics
        groups = GroupRegistration.objects.filter(event_id=event_id)
        analytics.total_groups = groups.count()
        analytics.total_group_members = sum(g.current_size for g in groups)
        
        # Calculate capacity utilization
        try:
            capacity_rule = CapacityRule.objects.get(event_id=event_id)
            analytics.capacity_utilization = analytics.calculate_utilization(
                capacity_rule.max_capacity
            )
        except CapacityRule.DoesNotExist:
            analytics.capacity_utilization = 0
        
        analytics.save()
        return analytics


class RegistrationReportService:
    """Service for generating registration reports."""
    
    def execute(self, event_id: uuid.UUID) -> Dict[str, Any]:
        """Generate comprehensive registration report."""
        analytics_service = GenerateAnalyticsService()
        analytics = analytics_service.execute(event_id)
        
        return {
            'event_id': str(event_id),
            'registrations': {
                'total': analytics.total_registrations,
                'confirmed': analytics.confirmed_registrations,
                'cancelled': analytics.cancelled_registrations,
            },
            'waitlist': {
                'total': analytics.total_waitlist,
                'promoted': analytics.promoted_from_waitlist,
                'conversion_rate': float(analytics.get_conversion_rate()),
            },
            'groups': {
                'total_groups': analytics.total_groups,
                'total_members': analytics.total_group_members,
            },
            'capacity': {
                'utilization': float(analytics.capacity_utilization),
            },
        }
