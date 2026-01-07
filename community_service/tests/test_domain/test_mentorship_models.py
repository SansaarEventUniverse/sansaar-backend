import pytest
from django.core.exceptions import ValidationError
from domain.models import MentorshipProgram, MentorMentee

@pytest.mark.django_db
class TestMentorshipProgram:
    def test_create_mentorship_program(self):
        program = MentorshipProgram.objects.create(
            title='Python Mentorship',
            description='Learn Python programming',
            skills_required='Python, Django',
            duration_weeks=12
        )
        assert program.title == 'Python Mentorship'
        assert program.is_active() is True
    
    def test_complete_program(self):
        program = MentorshipProgram.objects.create(
            title='Test Program',
            description='Test',
            skills_required='Testing',
            duration_weeks=8
        )
        program.complete()
        assert program.status == 'completed'
    
    def test_cancel_program(self):
        program = MentorshipProgram.objects.create(
            title='Test Program',
            description='Test',
            skills_required='Testing',
            duration_weeks=8
        )
        program.cancel()
        assert program.status == 'cancelled'

@pytest.mark.django_db
class TestMentorMentee:
    def test_create_relationship(self):
        program = MentorshipProgram.objects.create(
            title='Test',
            description='Test',
            skills_required='Test',
            duration_weeks=10
        )
        relationship = MentorMentee.objects.create(
            program=program,
            mentor_user_id=1,
            mentee_user_id=2
        )
        assert relationship.mentor_user_id == 1
        assert relationship.mentee_user_id == 2
        assert relationship.status == 'pending'
    
    def test_activate_relationship(self):
        program = MentorshipProgram.objects.create(
            title='Test',
            description='Test',
            skills_required='Test',
            duration_weeks=10
        )
        relationship = MentorMentee.objects.create(
            program=program,
            mentor_user_id=1,
            mentee_user_id=2
        )
        relationship.activate()
        assert relationship.is_active() is True
    
    def test_complete_relationship(self):
        program = MentorshipProgram.objects.create(
            title='Test',
            description='Test',
            skills_required='Test',
            duration_weeks=10
        )
        relationship = MentorMentee.objects.create(
            program=program,
            mentor_user_id=1,
            mentee_user_id=2,
            status='active'
        )
        relationship.complete()
        assert relationship.status == 'completed'
    
    def test_cannot_mentor_self(self):
        program = MentorshipProgram.objects.create(
            title='Test',
            description='Test',
            skills_required='Test',
            duration_weeks=10
        )
        relationship = MentorMentee(
            program=program,
            mentor_user_id=1,
            mentee_user_id=1
        )
        with pytest.raises(ValidationError):
            relationship.clean()
