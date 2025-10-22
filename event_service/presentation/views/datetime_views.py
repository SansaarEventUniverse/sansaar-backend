import uuid
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from django.core.exceptions import ValidationError

from application.datetime_service import ICalExportService
from infrastructure.services.timezone_service import TimezoneDatabase


@api_view(['GET'])
def export_ical(request, event_id):
    """Export event as iCal file."""
    try:
        service = ICalExportService()
        ical_content = service.execute(uuid.UUID(event_id))
        
        response = HttpResponse(ical_content, content_type='text/calendar')
        response['Content-Disposition'] = f'attachment; filename="event_{event_id}.ics"'
        return response
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
    except ValueError:
        return Response({'error': 'Invalid event ID'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def list_timezones(request):
    """List available timezones."""
    service = TimezoneDatabase()
    common = request.query_params.get('common', 'true').lower() == 'true'
    
    if common:
        timezones = service.get_common_timezones()
    else:
        timezones = service.get_all_timezones()
    
    return Response({'timezones': timezones})
