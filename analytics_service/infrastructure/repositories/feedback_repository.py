from domain.models import EventFeedback

class FeedbackRepository:
    def get_positive_feedback(self, event_id):
        return EventFeedback.objects.filter(event_id=event_id, rating__gte=4, status='approved')
    
    def get_negative_feedback(self, event_id):
        return EventFeedback.objects.filter(event_id=event_id, rating__lte=2, status='approved')
