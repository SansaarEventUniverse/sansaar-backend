import pytest
from rest_framework.test import APIClient
from domain.models import Feedback

@pytest.mark.django_db
class TestFeedbackAPI:
    def test_submit_event_feedback(self):
        client = APIClient()
        data = {
            'feedback_type': 'event',
            'entity_id': 1,
            'user_name': 'John Doe',
            'user_email': 'john@example.com',
            'rating': 5,
            'comment': 'Great event!'
        }
        response = client.post('/api/community/feedback/submit/', data, format='json')
        assert response.status_code == 201
        assert response.data['rating'] == 5
    
    def test_submit_forum_feedback(self):
        client = APIClient()
        data = {
            'feedback_type': 'forum',
            'entity_id': 2,
            'user_name': 'Jane',
            'user_email': 'jane@example.com',
            'rating': 4,
            'comment': 'Good discussion'
        }
        response = client.post('/api/community/feedback/submit/', data, format='json')
        assert response.status_code == 201
        assert response.data['feedback_type'] == 'forum'
    
    def test_get_feedback(self):
        Feedback.objects.create(feedback_type='volunteer', entity_id=3, user_name="Test", user_email="test@example.com", rating=5, comment="Great", status="approved")
        client = APIClient()
        response = client.get('/api/community/feedback/?type=volunteer&entity_id=3')
        assert response.status_code == 200
        assert len(response.data['results']) == 1
    
    def test_feedback_analytics(self):
        Feedback.objects.create(feedback_type='event', entity_id=1, user_name="A", user_email="a@test.com", rating=5, comment="Great", status="approved")
        Feedback.objects.create(feedback_type='event', entity_id=1, user_name="B", user_email="b@test.com", rating=4, comment="Good", status="approved")
        client = APIClient()
        response = client.get('/api/community/feedback/analytics/?type=event&entity_id=1')
        assert response.status_code == 200
        assert response.data['total'] == 2
        assert response.data['positive'] == 2
    
    def test_validation_invalid_rating(self):
        client = APIClient()
        data = {
            'feedback_type': 'event',
            'entity_id': 1,
            'user_name': 'Test',
            'user_email': 'test@example.com',
            'rating': 6,
            'comment': 'Invalid'
        }
        response = client.post('/api/community/feedback/submit/', data, format='json')
        assert response.status_code == 400
        assert 'rating' in response.data
