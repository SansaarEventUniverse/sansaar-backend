from domain.models import VolunteerOpportunity, VolunteerSkill

class CreateOpportunityService:
    def create(self, data):
        skills_data = data.pop('skills', [])
        opportunity = VolunteerOpportunity.objects.create(**data)
        for skill_data in skills_data:
            VolunteerSkill.objects.create(opportunity=opportunity, **skill_data)
        return opportunity
