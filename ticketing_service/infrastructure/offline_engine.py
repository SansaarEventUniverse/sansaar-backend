import uuid
from typing import Dict, Any, List
from datetime import timedelta
from django.utils import timezone

from domain.offline import OfflineTicket


class OfflineValidationEngine:
    """Engine for offline validation."""
    
    def validate(self, qr_code: str) -> Dict[str, Any]:
        """Validate ticket using offline engine."""
        try:
            ticket = OfflineTicket.objects.get(qr_code=qr_code)
        except OfflineTicket.DoesNotExist:
            return {'valid': False, 'reason': 'Ticket not found'}
        
        if not ticket.is_valid():
            return {'valid': False, 'reason': 'Ticket expired or invalid'}
        
        if ticket.status == 'used':
            return {'valid': False, 'reason': 'Ticket already used'}
        
        return {
            'valid': True,
            'ticket_id': str(ticket.ticket_id),
            'attendee_name': ticket.attendee_name
        }


class TicketDataSync:
    """Ticket data synchronization."""
    
    def sync_from_server(self, event_id: uuid.UUID, tickets: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Sync tickets from server."""
        synced = []
        
        for ticket_data in tickets:
            ticket, created = OfflineTicket.objects.update_or_create(
                ticket_id=ticket_data['ticket_id'],
                defaults={
                    'qr_code': ticket_data['qr_code'],
                    'event_id': event_id,
                    'attendee_name': ticket_data['attendee_name'],
                    'status': ticket_data.get('status', 'active'),
                    'valid_until': ticket_data['valid_until']
                }
            )
            synced.append(str(ticket.id))
        
        return {
            'synced_count': len(synced),
            'synced_ids': synced
        }


class OfflineAnalytics:
    """Offline analytics tracking."""
    
    def track_validation(self, ticket_id: uuid.UUID) -> Dict[str, Any]:
        """Track offline validation."""
        return {
            'ticket_id': str(ticket_id),
            'validated_at': timezone.now().isoformat(),
            'mode': 'offline'
        }


class ConflictResolution:
    """Conflict resolution for offline data."""
    
    def resolve(self, local_ticket: OfflineTicket, server_data: Dict[str, Any]) -> OfflineTicket:
        """Resolve conflicts between local and server data."""
        # Server data takes precedence
        local_ticket.status = server_data.get('status', local_ticket.status)
        local_ticket.valid_until = server_data.get('valid_until', local_ticket.valid_until)
        local_ticket.save()
        
        return local_ticket
