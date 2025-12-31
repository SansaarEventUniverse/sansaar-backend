from domain.models import VolunteerOpportunity

class SkillMatcher:
    def find_matching_opportunities(self, volunteer_skills):
        opportunities = VolunteerOpportunity.objects.filter(status='open').prefetch_related('skills')
        matches = []
        
        for opportunity in opportunities:
            required_skills = opportunity.skills.all()
            if not required_skills:
                matches.append({'opportunity': opportunity, 'match_score': 100})
                continue
            
            matched = sum(1 for skill in required_skills if skill.skill_name in volunteer_skills)
            total = required_skills.count()
            match_score = int((matched / total) * 100)
            
            if match_score > 0:
                matches.append({'opportunity': opportunity, 'match_score': match_score})
        
        return sorted(matches, key=lambda x: x['match_score'], reverse=True)
