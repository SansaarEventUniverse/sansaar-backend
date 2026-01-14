from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from application.services.moderation_service import ModerationService, SafetyMonitoringService, AutoModerationService
from infrastructure.repositories.moderation_repository import ModerationRepository
from presentation.serializers.moderation_serializers import ModerationRuleSerializer, ModerationActionSerializer

@api_view(['GET'])
def moderation_dashboard(request):
    """Get moderation dashboard statistics"""
    repo = ModerationRepository()
    stats = repo.get_moderation_stats()
    
    service = SafetyMonitoringService()
    pending_actions = service.get_pending_actions()
    serializer = ModerationActionSerializer(pending_actions, many=True)
    
    return Response({
        'stats': stats,
        'pending_actions': serializer.data
    })

@api_view(['POST'])
def report_content(request, content_id):
    """Report content for moderation"""
    target_type = request.data.get('target_type', 'content')
    reason = request.data.get('reason')
    
    if not reason:
        return Response({'error': 'reason is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    service = SafetyMonitoringService()
    action = service.create_action({
        'action_type': 'warning',
        'target_type': target_type,
        'target_id': content_id,
        'reason': reason
    })
    serializer = ModerationActionSerializer(action)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def moderation_actions(request):
    """Create or approve moderation actions"""
    action_id = request.data.get('action_id')
    action = request.data.get('action')
    
    if action == 'approve' and action_id:
        service = SafetyMonitoringService()
        updated = service.approve_action(int(action_id))
        serializer = ModerationActionSerializer(updated)
        return Response(serializer.data)
    
    return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
