from domain.models import VolunteerOpportunity

class OpportunityRepository:
    def get_active_opportunities(self):
        return VolunteerOpportunity.objects.filter(status='open')
    
    def get_by_location(self, location):
        return VolunteerOpportunity.objects.filter(location=location, status='open')
    
    def get_available_opportunities(self):
        return VolunteerOpportunity.objects.filter(
            status='open'
        ).exclude(
            volunteers_registered__gte=models.F('volunteers_needed')
        )
