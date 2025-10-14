class ListAllUsersService:
    def __init__(self, user_management_service):
        self.user_management_service = user_management_service

    def list_users(self, page: int = 1, limit: int = 50) -> dict:
        return self.user_management_service.get_users(page, limit)
