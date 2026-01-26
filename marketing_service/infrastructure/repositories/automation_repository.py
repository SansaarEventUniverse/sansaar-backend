from domain.models import AutomationWorkflow

class AutomationRepository:
    def get_analytics(self):
        total = AutomationWorkflow.objects.count()
        active = AutomationWorkflow.objects.filter(status='active').count()
        paused = AutomationWorkflow.objects.filter(status='paused').count()
        
        return {
            'total_workflows': total,
            'active': active,
            'paused': paused
        }
