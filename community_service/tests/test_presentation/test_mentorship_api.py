import pytest
from rest_framework.test import APIClient
from domain.models import MentorshipProgram, MentorMentee

@pytest.mark.django_db
class TestMentorshipAPI:
    def test_create_program(self):
        client = APIClient()
        data = {
            'title': 'Python Mentorship',
            'description': 'Learn Python programming',
            'skills_required': 'Python, Django',
            'duration_weeks': 12
        }
        response = client.post('/api/community/mentorship-programs/create/', data, format='json')
        assert response.status_code == 201
        assert response.data['title'] == 'Python Mentorship'
    
    def test_get_programs(self):
        MentorshipProgram.objects.create(title='P1', description='Test', skills_required='Test', duration_weeks=10)
        MentorshipProgram.objects.create(title='P2', description='Test', skills_required='Test', duration_weeks=8)
        client = APIClient()
        response = client.get('/api/community/mentorship-programs/')
        assert response.status_code == 200
        assert len(response.data['results']) == 2
    
    def test_join_program(self):
        program = MentorshipProgram.objects.create(title='Test', description='Test', skills_required='Test', duration_weeks=10)
        client = APIClient()
        data = {'mentor_user_id': 1, 'mentee_user_id': 2}
        response = client.post(f'/api/community/mentorship-programs/{program.id}/join/', data, format='json')
        assert response.status_code == 201
        assert response.data['mentor_user_id'] == 1
        assert response.data['mentee_user_id'] == 2
    
    def test_get_mentorships_as_mentee(self):
        program = MentorshipProgram.objects.create(title='Test', description='Test', skills_required='Test', duration_weeks=10)
        MentorMentee.objects.create(program=program, mentor_user_id=1, mentee_user_id=2, status='active')
        client = APIClient()
        response = client.get('/api/community/mentorships/?user_id=2&role=mentee')
        assert response.status_code == 200
        assert len(response.data['results']) == 1
    
    def test_get_mentorships_as_mentor(self):
        program = MentorshipProgram.objects.create(title='Test', description='Test', skills_required='Test', duration_weeks=10)
        MentorMentee.objects.create(program=program, mentor_user_id=1, mentee_user_id=2, status='active')
        MentorMentee.objects.create(program=program, mentor_user_id=1, mentee_user_id=3, status='active')
        client = APIClient()
        response = client.get('/api/community/mentorships/?user_id=1&role=mentor')
        assert response.status_code == 200
        assert len(response.data['results']) == 2
