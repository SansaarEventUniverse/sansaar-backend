from django.db import models
from domain.models import InterestGroup, GroupMembership
from django.db.models import Count

class InterestGroupRepository:
    def get_popular_groups(self, limit=5):
        return InterestGroup.objects.filter(is_active=True).annotate(
            member_count=Count('memberships', filter=models.Q(memberships__status='active'))
        ).order_by('-member_count')[:limit]
    
    def get_group_recommendations(self, user_id, limit=5):
        user_memberships = GroupMembership.objects.filter(
            user_id=user_id, status='active'
        ).values_list('group__category', flat=True)
        
        if not user_memberships:
            return self.get_popular_groups(limit)
        
        user_categories = set(user_memberships)
        user_group_ids = GroupMembership.objects.filter(
            user_id=user_id, status='active'
        ).values_list('group_id', flat=True)
        
        return InterestGroup.objects.filter(
            category__in=user_categories,
            is_active=True
        ).exclude(id__in=user_group_ids).annotate(
            member_count=Count('memberships', filter=models.Q(memberships__status='active'))
        ).order_by('-member_count')[:limit]
