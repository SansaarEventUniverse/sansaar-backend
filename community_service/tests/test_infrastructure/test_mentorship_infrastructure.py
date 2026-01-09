import pytest
from domain.models import MentorshipProgram, MentorMentee
from infrastructure.repositories.mentorship_repository import MentorshipRepository

@pytest.mark.django_db
class TestMentorshipRepository:
    def test_get_available_mentors(self):
        program = MentorshipProgram.objects.create(title='Test', description='Test', skills_required='Test', duration_weeks=10)
        MentorMentee.objects.create(program=program, mentor_user_id=1, mentee_user_id=2, status='active')
        MentorMentee.objects.create(program=program, mentor_user_id=1, mentee_user_id=3, status='active')
        MentorMentee.objects.create(program=program, mentor_user_id=4, mentee_user_id=5, status='active')
        
        repo = MentorshipRepository()
        available = repo.get_available_mentors(program.id, max_mentees=3)
        assert 1 in available
        assert 4 in available
    
    def test_get_mentorship_stats(self):
        program = MentorshipProgram.objects.create(title='Test', description='Test', skills_required='Test', duration_weeks=10)
        MentorMentee.objects.create(program=program, mentor_user_id=1, mentee_user_id=2, status='active')
        MentorMentee.objects.create(program=program, mentor_user_id=1, mentee_user_id=3, status='completed')
        MentorMentee.objects.create(program=program, mentor_user_id=4, mentee_user_id=5, status='pending')
        
        repo = MentorshipRepository()
        stats = repo.get_mentorship_stats(program.id)
        assert stats['total'] == 3
        assert stats['active'] == 1
        assert stats['completed'] == 1
