from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from application.list_sessions_service import ListSessionsService
from application.revoke_all_sessions_service import RevokeAllSessionsService
from application.revoke_session_service import RevokeSessionService


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_sessions(request):
    service = ListSessionsService()
    sessions = service.execute(request.user)
    
    # Get current session_id from JWT token
    current_session_id = None
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    if auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
        try:
            from infrastructure.services.jwt_service import JWTService
            jwt_service = JWTService()
            payload = jwt_service.decode_token(token)
            current_session_id = payload.get('session_id')
        except:
            pass
    
    data = [{
        'id': str(session.id),
        'ip_address': session.ip_address,
        'device_type': session.device_type,
        'browser': session.browser,
        'os': session.os,
        'location': session.location,
        'last_activity_at': session.last_activity_at,
        'created_at': session.created_at,
        'is_current': (session.id == current_session_id)
    } for session in sessions]
    
    return Response(data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def revoke_session(request, session_id):
    service = RevokeSessionService()
    result = service.execute(request.user, session_id)
    
    if not result:
        return Response({'error': 'Session not found'}, status=status.HTTP_404_NOT_FOUND)
    
    return Response({'message': 'Session revoked successfully'}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def revoke_all_sessions(request):
    service = RevokeAllSessionsService()
    count = service.execute(request.user)
    
    return Response({
        'message': 'All sessions revoked successfully',
        'revoked_count': count
    }, status=status.HTTP_200_OK)
