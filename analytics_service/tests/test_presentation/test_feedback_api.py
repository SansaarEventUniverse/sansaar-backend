import pytest
from rest_framework.test import APIClient
from domain.models import EventFeedback

@pytest.mark.django_db
class TestFeedbackAPI:
    def test_submit_feedback(self):
        client = APIClient()
        data = {
            'attendee_name': 'John Doe',
            'attendee_email': 'john@example.com',
            'rating': 5,
            'comment': 'Great event!'
        }
        response = client.post('/api/analytics/events/1/feedback/', data, format='json')
        assert response.status_code == 201
        assert response.data['rating'] == 5
    
    def test_get_feedback(self):
        EventFeedback.objects.create(
            event_id=1,
            attendee_name="Test",
            attendee_email="test@example.com",
            rating=4,
            comment="Good",
            status="approved"
        )
        client = APIClient()
        response = client.get('/api/analytics/events/1/feedback/list/')
        assert response.status_code == 200
        assert len(response.data['results']) == 1
    
    def test_feedback_analytics(self):
        EventFeedback.objects.create(event_id=1, attendee_name="A", attendee_email="a@test.com", rating=5, comment="Great", status="approved")
        EventFeedback.objects.create(event_id=1, attendee_name="B", attendee_email="b@test.com", rating=4, comment="Good", status="approved")
        client = APIClient()
        response = client.get('/api/analytics/events/1/feedback/analytics/')
        assert response.status_code == 200
        assert response.data['average_rating'] == 4.5
        assert response.data['total_feedback'] == 2
