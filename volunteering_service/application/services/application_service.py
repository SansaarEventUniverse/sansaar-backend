from domain.models import VolunteerApplication, VolunteerOpportunity

class ApplicationService:
    def create(self, data):
        opportunity_id = data.pop('opportunity_id')
        opportunity = VolunteerOpportunity.objects.get(id=opportunity_id)
        application = VolunteerApplication.objects.create(opportunity=opportunity, **data)
        return application
    
    def get_by_opportunity(self, opportunity_id):
        return VolunteerApplication.objects.filter(opportunity_id=opportunity_id)
