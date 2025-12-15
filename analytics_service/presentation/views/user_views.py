from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from application.services.user_management_service import UserManagementService
from application.services.user_activity_service import UserActivityService
from infrastructure.repositories.user_repository import UserRepository
from presentation.serializers.user_serializers import UserAnalyticsSerializer, UserActivitySerializer


class UserAnalyticsAPI(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({'error': 'user_id required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            service = UserManagementService()
            analytics = service.get_user_analytics(user_id)
            serializer = UserAnalyticsSerializer(analytics)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)


class UserActivityAPI(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({'error': 'user_id required'}, status=status.HTTP_400_BAD_REQUEST)
        
        service = UserActivityService()
        activities = service.get_user_activities(user_id)
        serializer = UserActivitySerializer(activities, many=True)
        return Response(serializer.data)


class UsersListAPI(APIView):
    def get(self, request):
        repo = UserRepository()
        users = repo.get_all_users()
        serializer = UserAnalyticsSerializer(users, many=True)
        return Response(serializer.data)
