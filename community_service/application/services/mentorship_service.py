from domain.models import MentorshipProgram, MentorMentee

class MentorshipService:
    def create_program(self, data):
        return MentorshipProgram.objects.create(**data)
    
    def get_active_programs(self):
        return MentorshipProgram.objects.filter(status='active')

class MentorMatchingService:
    def create_match(self, program_id, mentor_user_id, mentee_user_id):
        program = MentorshipProgram.objects.get(id=program_id)
        return MentorMentee.objects.create(
            program=program,
            mentor_user_id=mentor_user_id,
            mentee_user_id=mentee_user_id
        )
    
    def approve_match(self, match_id):
        match = MentorMentee.objects.get(id=match_id)
        match.activate()
        return match

class MentorshipTrackingService:
    def get_mentor_relationships(self, mentor_user_id):
        return MentorMentee.objects.filter(mentor_user_id=mentor_user_id, status='active')
    
    def get_mentee_relationships(self, mentee_user_id):
        return MentorMentee.objects.filter(mentee_user_id=mentee_user_id, status='active')
    
    def complete_relationship(self, match_id):
        match = MentorMentee.objects.get(id=match_id)
        match.complete()
        return match
