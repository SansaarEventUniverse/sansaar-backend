from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from application.services.connection_service import ConnectionManagementService
from infrastructure.repositories.connection_repository import ConnectionRepository
from presentation.serializers.connection_serializers import ConnectionSerializer

@api_view(['POST'])
def connect_user(request):
    from_user_id = request.data.get('from_user_id')
    to_user_id = request.data.get('to_user_id')
    
    if not from_user_id or not to_user_id:
        return Response({'error': 'from_user_id and to_user_id are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    service = ConnectionManagementService()
    connection = service.send_connection_request(int(from_user_id), int(to_user_id))
    serializer = ConnectionSerializer(connection)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_connections(request):
    user_id = request.query_params.get('user_id')
    
    if not user_id:
        return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    service = ConnectionManagementService()
    connections = service.get_user_connections(int(user_id))
    serializer = ConnectionSerializer(connections, many=True)
    return Response({'results': serializer.data})

@api_view(['PUT'])
def update_connection_status(request, connection_id):
    action = request.data.get('action')
    
    if action not in ['accept', 'reject']:
        return Response({'error': 'action must be accept or reject'}, status=status.HTTP_400_BAD_REQUEST)
    
    service = ConnectionManagementService()
    if action == 'accept':
        connection = service.accept_connection(connection_id)
    else:
        connection = service.reject_connection(connection_id)
    
    serializer = ConnectionSerializer(connection)
    return Response(serializer.data)

@api_view(['GET'])
def get_recommendations(request):
    user_id = request.query_params.get('user_id')
    
    if not user_id:
        return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    repo = ConnectionRepository()
    recommendations = repo.get_connection_recommendations(int(user_id), limit=5)
    return Response({'recommendations': recommendations})
