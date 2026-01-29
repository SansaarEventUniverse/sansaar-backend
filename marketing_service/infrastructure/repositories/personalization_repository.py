from domain.models import PersonalizationRule

class PersonalizationRepository:
    def get_analytics(self):
        total = PersonalizationRule.objects.count()
        active = PersonalizationRule.objects.filter(is_active=True).count()
        inactive = PersonalizationRule.objects.filter(is_active=False).count()
        
        return {
            'total_rules': total,
            'active': active,
            'inactive': inactive
        }
