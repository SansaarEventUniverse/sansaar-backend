from typing import List, Dict, Any
import uuid

from domain.recommendation import UserPreference, RecommendationScore
from domain.search_index import EventSearchIndex


class UserPreferenceService:
    """Service for managing user preferences."""
    
    def get_or_create_preference(self, user_id: uuid.UUID) -> UserPreference:
        """Get or create user preference."""
        pref, created = UserPreference.objects.get_or_create(user_id=user_id)
        return pref
    
    def update_preferences(self, user_id: uuid.UUID, data: Dict[str, Any]) -> UserPreference:
        """Update user preferences."""
        pref = self.get_or_create_preference(user_id)
        
        if 'preferred_categories' in data:
            pref.preferred_categories = data['preferred_categories']
        if 'preferred_tags' in data:
            pref.preferred_tags = data['preferred_tags']
        if 'preferred_cities' in data:
            pref.preferred_cities = data['preferred_cities']
        
        pref.save()
        return pref


class EventRecommendationService:
    """Service for generating event recommendations."""
    
    def generate_recommendations(self, user_id: uuid.UUID, limit: int = 10) -> List[Dict[str, Any]]:
        """Generate personalized event recommendations."""
        # Get user preferences
        try:
            pref = UserPreference.objects.get(user_id=user_id)
        except UserPreference.DoesNotExist:
            # Return popular events for new users
            return self._get_popular_events(limit)
        
        # Get published events
        events = EventSearchIndex.objects.filter(is_published=True)
        
        recommendations = []
        for event in events:
            score = self._calculate_event_score(event, pref)
            if score > 0:
                recommendations.append({
                    'event_id': str(event.event_id),
                    'title': event.title,
                    'category': event.category,
                    'score': round(score, 2),
                    'reason': self._generate_reason(event, pref),
                })
        
        # Sort by score and return top N
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations[:limit]
    
    def _calculate_event_score(self, event: EventSearchIndex, pref: UserPreference) -> float:
        """Calculate recommendation score for an event."""
        score = 0.0
        
        # Category match
        if event.category in pref.preferred_categories:
            score += 0.3
        
        # Tag match
        matching_tags = set(event.tags) & set(pref.preferred_tags)
        if matching_tags:
            score += 0.25 * (len(matching_tags) / max(len(pref.preferred_tags), 1))
        
        # City match
        if event.city in pref.preferred_cities:
            score += 0.25
        
        # Popularity
        score += min(event.view_count / 1000, 0.2)
        
        return score
    
    def _generate_reason(self, event: EventSearchIndex, pref: UserPreference) -> str:
        """Generate explanation for recommendation."""
        reasons = []
        
        if event.category in pref.preferred_categories:
            reasons.append(f"Matches your interest in {event.category}")
        
        matching_tags = set(event.tags) & set(pref.preferred_tags)
        if matching_tags:
            reasons.append(f"Tagged with {', '.join(list(matching_tags)[:2])}")
        
        if event.city in pref.preferred_cities:
            reasons.append(f"In your preferred city {event.city}")
        
        return '; '.join(reasons) if reasons else "Popular event"
    
    def _get_popular_events(self, limit: int) -> List[Dict[str, Any]]:
        """Get popular events for users without preferences."""
        events = EventSearchIndex.objects.filter(is_published=True).order_by('-search_rank')[:limit]
        
        return [
            {
                'event_id': str(e.event_id),
                'title': e.title,
                'category': e.category,
                'score': e.search_rank / 100,
                'reason': 'Popular event',
            }
            for e in events
        ]


class SimilarEventsService:
    """Service for finding similar events."""
    
    def find_similar(self, event_id: uuid.UUID, limit: int = 5) -> List[EventSearchIndex]:
        """Find events similar to given event."""
        try:
            event = EventSearchIndex.objects.get(event_id=event_id)
        except EventSearchIndex.DoesNotExist:
            return []
        
        # Find events with same category or overlapping tags
        similar = EventSearchIndex.objects.filter(
            is_published=True
        ).exclude(event_id=event_id)
        
        # Filter by category
        similar = similar.filter(category=event.category)
        
        return list(similar.order_by('-search_rank')[:limit])
