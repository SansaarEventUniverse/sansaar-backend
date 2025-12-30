from domain.models import VolunteerOpportunity

class ManageOpportunityService:
    def update(self, opportunity_id, data):
        opportunity = VolunteerOpportunity.objects.get(id=opportunity_id)
        for key, value in data.items():
            setattr(opportunity, key, value)
        opportunity.save()
        return opportunity
    
    def close(self, opportunity_id):
        opportunity = VolunteerOpportunity.objects.get(id=opportunity_id)
        opportunity.status = 'closed'
        opportunity.save()
        return opportunity
