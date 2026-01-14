from domain.models import ModerationAction, ModerationRule
from django.db.models import Count

class ModerationRepository:
    def get_moderation_stats(self):
        """Get comprehensive moderation statistics"""
        total_actions = ModerationAction.objects.count()
        pending = ModerationAction.objects.filter(status='pending').count()
        approved = ModerationAction.objects.filter(status='approved').count()
        rejected = ModerationAction.objects.filter(status='rejected').count()
        
        return {
            'total_actions': total_actions,
            'pending': pending,
            'approved': approved,
            'rejected': rejected
        }
    
    def get_rule_effectiveness(self, rule_id):
        """Calculate rule effectiveness based on actions"""
        actions = ModerationAction.objects.filter(rule_id=rule_id)
        total = actions.count()
        approved = actions.filter(status='approved').count()
        
        effectiveness = (approved / total * 100) if total > 0 else 0
        
        return {
            'rule_id': rule_id,
            'total_actions': total,
            'approved_actions': approved,
            'effectiveness': effectiveness
        }
