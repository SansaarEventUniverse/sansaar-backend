from domain.models import Connection

class ConnectionRepository:
    def get_mutual_connections(self, user_id1, user_id2):
        user1_connections = set(
            Connection.objects.filter(from_user_id=user_id1, status='accepted').values_list('to_user_id', flat=True)
        ) | set(
            Connection.objects.filter(to_user_id=user_id1, status='accepted').values_list('from_user_id', flat=True)
        )
        
        user2_connections = set(
            Connection.objects.filter(from_user_id=user_id2, status='accepted').values_list('to_user_id', flat=True)
        ) | set(
            Connection.objects.filter(to_user_id=user_id2, status='accepted').values_list('from_user_id', flat=True)
        )
        
        return user1_connections & user2_connections
    
    def get_connection_recommendations(self, user_id, limit=5):
        user_connections = set(
            Connection.objects.filter(from_user_id=user_id, status='accepted').values_list('to_user_id', flat=True)
        ) | set(
            Connection.objects.filter(to_user_id=user_id, status='accepted').values_list('from_user_id', flat=True)
        )
        
        recommendations = {}
        for connection_id in user_connections:
            friends_of_friend = set(
                Connection.objects.filter(from_user_id=connection_id, status='accepted').values_list('to_user_id', flat=True)
            ) | set(
                Connection.objects.filter(to_user_id=connection_id, status='accepted').values_list('from_user_id', flat=True)
            )
            
            for user in friends_of_friend:
                if user != user_id and user not in user_connections:
                    recommendations[user] = recommendations.get(user, 0) + 1
        
        sorted_recommendations = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)
        return [user_id for user_id, _ in sorted_recommendations[:limit]]
