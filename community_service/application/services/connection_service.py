from domain.models import Connection

class ConnectionManagementService:
    def send_connection_request(self, from_user_id, to_user_id):
        connection = Connection.objects.create(from_user_id=from_user_id, to_user_id=to_user_id)
        return connection
    
    def accept_connection(self, connection_id):
        connection = Connection.objects.get(id=connection_id)
        connection.accept()
        return connection
    
    def reject_connection(self, connection_id):
        connection = Connection.objects.get(id=connection_id)
        connection.reject()
        return connection
    
    def get_user_connections(self, user_id):
        return Connection.objects.filter(
            from_user_id=user_id, status='accepted'
        ) | Connection.objects.filter(
            to_user_id=user_id, status='accepted'
        )
    
    def get_pending_requests(self, user_id):
        return Connection.objects.filter(to_user_id=user_id, status='pending')
