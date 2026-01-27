from domain.models import ABTest

class ABTestingRepository:
    def get_analytics(self):
        total = ABTest.objects.count()
        running = ABTest.objects.filter(status='running').count()
        completed = ABTest.objects.filter(status='completed').count()
        
        return {
            'total_tests': total,
            'running': running,
            'completed': completed
        }
