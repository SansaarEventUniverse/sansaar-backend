import pytest
from django.core.exceptions import ValidationError
from domain.models import EventFeedback

@pytest.mark.django_db
class TestEventFeedback:
    def test_create_feedback(self):
        feedback = EventFeedback.objects.create(
            event_id=1,
            attendee_name="John Doe",
            attendee_email="john@example.com",
            rating=5,
            comment="Great event!",
            status="approved"
        )
        assert feedback.rating == 5
        assert feedback.status == "approved"
    
    def test_feedback_is_positive(self):
        feedback = EventFeedback.objects.create(
            event_id=1,
            attendee_name="Jane",
            attendee_email="jane@example.com",
            rating=5,
            comment="Excellent",
            status="approved"
        )
        assert feedback.is_positive() is True
    
    def test_feedback_is_negative(self):
        feedback = EventFeedback.objects.create(
            event_id=1,
            attendee_name="Bob",
            attendee_email="bob@example.com",
            rating=2,
            comment="Not good",
            status="approved"
        )
        assert feedback.is_negative() is True
    
    def test_feedback_approve(self):
        feedback = EventFeedback.objects.create(
            event_id=1,
            attendee_name="Alice",
            attendee_email="alice@example.com",
            rating=4,
            comment="Good event",
            status="pending"
        )
        feedback.approve()
        assert feedback.status == "approved"
    
    def test_rating_validation(self):
        with pytest.raises(ValidationError):
            feedback = EventFeedback(
                event_id=1,
                attendee_name="Test",
                attendee_email="test@example.com",
                rating=6,
                comment="Invalid rating",
                status="pending"
            )
            feedback.clean()
