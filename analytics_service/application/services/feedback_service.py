from domain.models import EventFeedback

class FeedbackService:
    def create(self, data):
        return EventFeedback.objects.create(**data)
    
    def get_by_event(self, event_id):
        return EventFeedback.objects.filter(event_id=event_id, status='approved')

class RatingAnalysisService:
    def calculate_average_rating(self, event_id):
        feedbacks = EventFeedback.objects.filter(event_id=event_id, status='approved')
        if not feedbacks:
            return 0
        return sum(f.rating for f in feedbacks) / feedbacks.count()
