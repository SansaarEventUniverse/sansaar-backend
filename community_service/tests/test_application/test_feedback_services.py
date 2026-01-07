import pytest
from domain.models import Feedback
from application.services.feedback_service import FeedbackService

@pytest.mark.django_db
class TestFeedbackService:
    def test_create_feedback(self):
        service = FeedbackService()
        data = {
            'feedback_type': 'event',
            'entity_id': 1,
            'user_name': 'John',
            'user_email': 'john@example.com',
            'rating': 5,
            'comment': 'Great!'
        }
        feedback = service.create(data)
        assert feedback.rating == 5
    
    def test_get_by_entity(self):
        Feedback.objects.create(feedback_type='event', entity_id=1, user_name="A", user_email="a@test.com", rating=5, comment="Good", status="approved")
        Feedback.objects.create(feedback_type='event', entity_id=1, user_name="B", user_email="b@test.com", rating=4, comment="Nice", status="pending")
        service = FeedbackService()
        feedbacks = service.get_by_entity('event', 1)
        assert feedbacks.count() == 1
    
    def test_calculate_average_rating(self):
        Feedback.objects.create(feedback_type='forum', entity_id=2, user_name="A", user_email="a@test.com", rating=5, comment="Great", status="approved")
        Feedback.objects.create(feedback_type='forum', entity_id=2, user_name="B", user_email="b@test.com", rating=3, comment="OK", status="approved")
        service = FeedbackService()
        avg = service.calculate_average_rating('forum', 2)
        assert avg == 4.0
