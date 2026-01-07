from domain.models import Feedback

class FeedbackService:
    def create(self, data):
        return Feedback.objects.create(**data)
    
    def get_by_entity(self, feedback_type, entity_id):
        return Feedback.objects.filter(feedback_type=feedback_type, entity_id=entity_id, status='approved')
    
    def calculate_average_rating(self, feedback_type, entity_id):
        feedbacks = Feedback.objects.filter(feedback_type=feedback_type, entity_id=entity_id, status='approved')
        if not feedbacks:
            return 0
        return sum(f.rating for f in feedbacks) / feedbacks.count()
