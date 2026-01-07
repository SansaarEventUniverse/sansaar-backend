import pytest
from domain.models import Feedback
from infrastructure.repositories.feedback_repository import FeedbackRepository

@pytest.mark.django_db
class TestFeedbackRepository:
    def test_get_positive_feedback(self):
        Feedback.objects.create(feedback_type='event', entity_id=1, user_name="A", user_email="a@test.com", rating=5, comment="Great", status="approved")
        Feedback.objects.create(feedback_type='event', entity_id=1, user_name="B", user_email="b@test.com", rating=2, comment="Bad", status="approved")
        repo = FeedbackRepository()
        positive = repo.get_positive_feedback('event', 1)
        assert positive.count() == 1
    
    def test_get_negative_feedback(self):
        Feedback.objects.create(feedback_type='volunteer', entity_id=2, user_name="A", user_email="a@test.com", rating=1, comment="Poor", status="approved")
        Feedback.objects.create(feedback_type='volunteer', entity_id=2, user_name="B", user_email="b@test.com", rating=5, comment="Excellent", status="approved")
        repo = FeedbackRepository()
        negative = repo.get_negative_feedback('volunteer', 2)
        assert negative.count() == 1
    
    def test_get_feedback_stats(self):
        Feedback.objects.create(feedback_type='forum', entity_id=3, user_name="A", user_email="a@test.com", rating=5, comment="Great", status="approved")
        Feedback.objects.create(feedback_type='forum', entity_id=3, user_name="B", user_email="b@test.com", rating=4, comment="Good", status="approved")
        Feedback.objects.create(feedback_type='forum', entity_id=3, user_name="C", user_email="c@test.com", rating=2, comment="Bad", status="approved")
        repo = FeedbackRepository()
        stats = repo.get_feedback_stats('forum', 3)
        assert stats['total'] == 3
        assert stats['positive'] == 2
        assert stats['negative'] == 1
        assert stats['average'] == 3.67
