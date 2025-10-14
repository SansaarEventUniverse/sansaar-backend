from django.test import RequestFactory

from infrastructure.middleware.jwt_middleware import SuperAdminJWTMiddleware
from infrastructure.services.jwt_service import JWTService


class TestSuperAdminJWTMiddleware:
    def test_exempt_paths(self):
        factory = RequestFactory()
        request = factory.get("/api/superadmin/health/")

        def get_response(req):
            return "OK"

        middleware = SuperAdminJWTMiddleware(get_response)
        response = middleware(request)
        assert response == "OK"

    def test_missing_auth_header(self):
        factory = RequestFactory()
        request = factory.get("/api/superadmin/protected/")

        def get_response(req):
            return "OK"

        middleware = SuperAdminJWTMiddleware(get_response)
        response = middleware(request)
        assert response.status_code == 401

    def test_valid_token(self):
        jwt_service = JWTService()
        token = jwt_service.generate_token("admin-123", "admin@example.com")

        factory = RequestFactory()
        request = factory.get("/api/superadmin/protected/", HTTP_AUTHORIZATION=f"Bearer {token}")

        def get_response(req):
            assert req.superadmin_id == "admin-123"
            assert req.superadmin_email == "admin@example.com"
            return "OK"

        middleware = SuperAdminJWTMiddleware(get_response)
        response = middleware(request)
        assert response == "OK"

    def test_invalid_token(self):
        factory = RequestFactory()
        request = factory.get("/api/superadmin/protected/", HTTP_AUTHORIZATION="Bearer invalid_token")

        def get_response(req):
            return "OK"

        middleware = SuperAdminJWTMiddleware(get_response)
        response = middleware(request)
        assert response.status_code == 401
