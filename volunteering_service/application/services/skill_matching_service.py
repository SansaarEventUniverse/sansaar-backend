from domain.models import VolunteerOpportunity

class SkillMatchingService:
    def calculate_match_score(self, opportunity_id, volunteer_skills):
        opportunity = VolunteerOpportunity.objects.get(id=opportunity_id)
        required_skills = opportunity.skills.all()
        
        if not required_skills:
            return 100
        
        matched = sum(1 for skill in required_skills if skill.skill_name in volunteer_skills)
        total = required_skills.count()
        return int((matched / total) * 100)
