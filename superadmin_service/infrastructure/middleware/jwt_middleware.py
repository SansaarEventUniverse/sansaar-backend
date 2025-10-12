import jwt
from django.http import JsonResponse

from infrastructure.services.jwt_service import JWTService


class SuperAdminJWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_service = JWTService()
        self.exempt_paths = ["/api/superadmin/health/", "/api/superadmin/auth/login/", "/admin/"]

    def __call__(self, request):
        if any(request.path.startswith(path) for path in self.exempt_paths):
            return self.get_response(request)

        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JsonResponse({"error": "Authorization header required"}, status=401)

        token = auth_header.split(" ")[1]

        try:
            payload = self.jwt_service.verify_token(token)
            request.superadmin_id = payload.get("admin_id")
            request.superadmin_email = payload.get("email")
        except jwt.InvalidTokenError as e:
            return JsonResponse({"error": str(e)}, status=401)

        return self.get_response(request)
