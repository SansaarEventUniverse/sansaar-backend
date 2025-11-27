import uuid
from datetime import timedelta
from typing import Dict, Any, List
from django.core.exceptions import ValidationError
from django.utils import timezone

from domain.offline import OfflineTicket, ValidationCache


class OfflineValidationService:
    """Service for offline ticket validation."""
    
    def validate_ticket(self, qr_code: str) -> Dict[str, Any]:
        """Validate ticket offline."""
        try:
            ticket = OfflineTicket.objects.get(qr_code=qr_code)
        except OfflineTicket.DoesNotExist:
            raise ValidationError("Ticket not found")
        
        ticket.validate_offline()
        ticket.mark_used()
        
        return {
            'ticket_id': str(ticket.ticket_id),
            'status': 'validated',
            'attendee_name': ticket.attendee_name
        }


class TicketSyncService:
    """Service for ticket synchronization."""
    
    def sync_tickets(self, event_id: uuid.UUID, tickets: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Sync tickets for offline use."""
        synced_count = 0
        
        for ticket_data in tickets:
            OfflineTicket.objects.update_or_create(
                ticket_id=ticket_data['ticket_id'],
                defaults={
                    'qr_code': ticket_data['qr_code'],
                    'event_id': event_id,
                    'attendee_name': ticket_data['attendee_name'],
                    'status': ticket_data.get('status', 'active'),
                    'valid_until': ticket_data['valid_until']
                }
            )
            synced_count += 1
        
        return {
            'event_id': str(event_id),
            'synced_count': synced_count,
            'synced_at': timezone.now().isoformat()
        }


class CacheManagementService:
    """Service for cache management."""
    
    def create_cache(self, event_id: uuid.UUID, data: Dict[str, Any]) -> ValidationCache:
        """Create validation cache."""
        expires_at = timezone.now() + timedelta(hours=24)
        
        cache = ValidationCache.objects.create(
            event_id=event_id,
            cache_data=data,
            ticket_count=len(data.get('tickets', [])),
            expires_at=expires_at
        )
        
        return cache
    
    def get_cache(self, event_id: uuid.UUID) -> ValidationCache:
        """Get validation cache."""
        try:
            cache = ValidationCache.objects.get(event_id=event_id)
            if cache.is_expired():
                raise ValidationError("Cache expired")
            return cache
        except ValidationCache.DoesNotExist:
            raise ValidationError("Cache not found")
