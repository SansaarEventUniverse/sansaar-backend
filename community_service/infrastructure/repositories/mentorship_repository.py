from domain.models import MentorMentee, MentorshipProgram
from django.db.models import Count, Q

class MentorshipRepository:
    def get_available_mentors(self, program_id, max_mentees=5):
        active_mentors = MentorMentee.objects.filter(
            program_id=program_id,
            status='active'
        ).values('mentor_user_id').annotate(
            mentee_count=Count('id')
        ).filter(mentee_count__lt=max_mentees).values_list('mentor_user_id', flat=True)
        
        return list(active_mentors)
    
    def get_mentorship_stats(self, program_id):
        total = MentorMentee.objects.filter(program_id=program_id).count()
        active = MentorMentee.objects.filter(program_id=program_id, status='active').count()
        completed = MentorMentee.objects.filter(program_id=program_id, status='completed').count()
        
        return {
            'total': total,
            'active': active,
            'completed': completed
        }
