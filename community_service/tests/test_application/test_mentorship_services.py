import pytest
from domain.models import MentorshipProgram, MentorMentee
from application.services.mentorship_service import MentorshipService, MentorMatchingService, MentorshipTrackingService

@pytest.mark.django_db
class TestMentorshipService:
    def test_create_program(self):
        service = MentorshipService()
        program = service.create_program({
            'title': 'Python Mentorship',
            'description': 'Learn Python',
            'skills_required': 'Python',
            'duration_weeks': 12
        })
        assert program.title == 'Python Mentorship'
    
    def test_get_active_programs(self):
        MentorshipProgram.objects.create(title='Active', description='Test', skills_required='Test', duration_weeks=10, status='active')
        MentorshipProgram.objects.create(title='Completed', description='Test', skills_required='Test', duration_weeks=10, status='completed')
        service = MentorshipService()
        programs = service.get_active_programs()
        assert programs.count() == 1

@pytest.mark.django_db
class TestMentorMatchingService:
    def test_create_match(self):
        program = MentorshipProgram.objects.create(title='Test', description='Test', skills_required='Test', duration_weeks=10)
        service = MentorMatchingService()
        match = service.create_match(program.id, 1, 2)
        assert match.mentor_user_id == 1
        assert match.mentee_user_id == 2
    
    def test_approve_match(self):
        program = MentorshipProgram.objects.create(title='Test', description='Test', skills_required='Test', duration_weeks=10)
        match = MentorMentee.objects.create(program=program, mentor_user_id=1, mentee_user_id=2)
        service = MentorMatchingService()
        updated = service.approve_match(match.id)
        assert updated.is_active()

@pytest.mark.django_db
class TestMentorshipTrackingService:
    def test_get_mentor_relationships(self):
        program = MentorshipProgram.objects.create(title='Test', description='Test', skills_required='Test', duration_weeks=10)
        MentorMentee.objects.create(program=program, mentor_user_id=1, mentee_user_id=2, status='active')
        MentorMentee.objects.create(program=program, mentor_user_id=1, mentee_user_id=3, status='active')
        service = MentorshipTrackingService()
        relationships = service.get_mentor_relationships(1)
        assert relationships.count() == 2
    
    def test_get_mentee_relationships(self):
        program = MentorshipProgram.objects.create(title='Test', description='Test', skills_required='Test', duration_weeks=10)
        MentorMentee.objects.create(program=program, mentor_user_id=1, mentee_user_id=2, status='active')
        service = MentorshipTrackingService()
        relationships = service.get_mentee_relationships(2)
        assert relationships.count() == 1
    
    def test_complete_relationship(self):
        program = MentorshipProgram.objects.create(title='Test', description='Test', skills_required='Test', duration_weeks=10)
        match = MentorMentee.objects.create(program=program, mentor_user_id=1, mentee_user_id=2, status='active')
        service = MentorshipTrackingService()
        updated = service.complete_relationship(match.id)
        assert updated.status == 'completed'
