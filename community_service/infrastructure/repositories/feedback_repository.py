from domain.models import Feedback

class FeedbackRepository:
    def get_positive_feedback(self, feedback_type, entity_id):
        return Feedback.objects.filter(feedback_type=feedback_type, entity_id=entity_id, rating__gte=4, status='approved')
    
    def get_negative_feedback(self, feedback_type, entity_id):
        return Feedback.objects.filter(feedback_type=feedback_type, entity_id=entity_id, rating__lte=2, status='approved')
    
    def get_feedback_stats(self, feedback_type, entity_id):
        feedbacks = Feedback.objects.filter(feedback_type=feedback_type, entity_id=entity_id, status='approved')
        total = feedbacks.count()
        if total == 0:
            return {'total': 0, 'positive': 0, 'negative': 0, 'average': 0}
        
        positive = feedbacks.filter(rating__gte=4).count()
        negative = feedbacks.filter(rating__lte=2).count()
        average = sum(f.rating for f in feedbacks) / total
        
        return {
            'total': total,
            'positive': positive,
            'negative': negative,
            'average': round(average, 2)
        }
