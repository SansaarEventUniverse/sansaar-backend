class SuperAdminLogoutService:
    def __init__(self, jwt_service):
        self.jwt_service = jwt_service

    def logout(self, token: str) -> dict:
        self.jwt_service.blacklist_token(token)
        return {"message": "Logged out successfully"}
