import pytest
from django.core.exceptions import ValidationError
from domain.models import Feedback

@pytest.mark.django_db
class TestFeedback:
    def test_create_event_feedback(self):
        feedback = Feedback.objects.create(
            feedback_type='event',
            entity_id=1,
            user_name="John Doe",
            user_email="john@example.com",
            rating=5,
            comment="Great event!",
            status="approved"
        )
        assert feedback.rating == 5
        assert feedback.feedback_type == 'event'
    
    def test_create_forum_feedback(self):
        feedback = Feedback.objects.create(
            feedback_type='forum',
            entity_id=1,
            user_name="Jane",
            user_email="jane@example.com",
            rating=4,
            comment="Good discussion",
            status="approved"
        )
        assert feedback.feedback_type == 'forum'
    
    def test_create_volunteer_feedback(self):
        feedback = Feedback.objects.create(
            feedback_type='volunteer',
            entity_id=1,
            user_name="Bob",
            user_email="bob@example.com",
            rating=5,
            comment="Excellent volunteer",
            status="approved"
        )
        assert feedback.feedback_type == 'volunteer'
    
    def test_feedback_is_positive(self):
        feedback = Feedback.objects.create(
            feedback_type='event',
            entity_id=1,
            user_name="Alice",
            user_email="alice@example.com",
            rating=5,
            comment="Excellent",
            status="approved"
        )
        assert feedback.is_positive() is True
    
    def test_feedback_is_negative(self):
        feedback = Feedback.objects.create(
            feedback_type='event',
            entity_id=1,
            user_name="Charlie",
            user_email="charlie@example.com",
            rating=2,
            comment="Not good",
            status="approved"
        )
        assert feedback.is_negative() is True
    
    def test_feedback_approve(self):
        feedback = Feedback.objects.create(
            feedback_type='event',
            entity_id=1,
            user_name="Test",
            user_email="test@example.com",
            rating=4,
            comment="Good",
            status="pending"
        )
        feedback.approve()
        assert feedback.status == "approved"
    
    def test_rating_validation(self):
        with pytest.raises(ValidationError):
            feedback = Feedback(
                feedback_type='event',
                entity_id=1,
                user_name="Test",
                user_email="test@example.com",
                rating=6,
                comment="Invalid",
                status="pending"
            )
            feedback.clean()
