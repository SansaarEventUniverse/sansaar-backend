import pytest
import jwt
from django.conf import settings
from django.http import HttpRequest, JsonResponse
from infrastructure.middleware.permission_middleware import PermissionMiddleware


class TestPermissionMiddleware:
    def test_exempt_path_health(self):
        def get_response(request):
            return JsonResponse({'status': 'ok'})
        
        middleware = PermissionMiddleware(get_response)
        request = HttpRequest()
        request.path = '/api/role/health/'
        request.method = 'GET'
        
        response = middleware(request)
        assert response.status_code == 200
    
    def test_missing_token(self):
        def get_response(request):
            return JsonResponse({'status': 'ok'})
        
        middleware = PermissionMiddleware(get_response)
        request = HttpRequest()
        request.path = '/api/role/test/'
        request.method = 'GET'
        request.META = {}
        
        response = middleware(request)
        assert response.status_code == 401
        assert b'Authentication required' in response.content
    
    def test_valid_token(self):
        def get_response(request):
            return JsonResponse({'status': 'ok'})
        
        token = jwt.encode(
            {'user_id': 'user-123', 'session_id': 'session-456'},
            settings.SECRET_KEY,
            algorithm='HS256'
        )
        
        middleware = PermissionMiddleware(get_response)
        request = HttpRequest()
        request.path = '/api/role/test/'
        request.method = 'GET'
        request.META = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
        
        response = middleware(request)
        assert response.status_code == 200
        assert request.user_id == 'user-123'
        assert request.session_id == 'session-456'
    
    def test_expired_token(self):
        def get_response(request):
            return JsonResponse({'status': 'ok'})
        
        import time
        token = jwt.encode(
            {'user_id': 'user-123', 'exp': int(time.time()) - 100},
            settings.SECRET_KEY,
            algorithm='HS256'
        )
        
        middleware = PermissionMiddleware(get_response)
        request = HttpRequest()
        request.path = '/api/role/test/'
        request.method = 'GET'
        request.META = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
        
        response = middleware(request)
        assert response.status_code == 401
        assert b'Token expired' in response.content
    
    def test_invalid_token(self):
        def get_response(request):
            return JsonResponse({'status': 'ok'})
        
        middleware = PermissionMiddleware(get_response)
        request = HttpRequest()
        request.path = '/api/role/test/'
        request.method = 'GET'
        request.META = {'HTTP_AUTHORIZATION': 'Bearer invalid-token'}
        
        response = middleware(request)
        assert response.status_code == 401
        assert b'Invalid token' in response.content
    
    def test_extract_token_with_bearer(self):
        def get_response(request):
            return JsonResponse({'status': 'ok'})
        
        middleware = PermissionMiddleware(get_response)
        request = HttpRequest()
        request.META = {'HTTP_AUTHORIZATION': 'Bearer test-token'}
        
        token = middleware.extract_token(request)
        assert token == 'test-token'
    
    def test_extract_token_without_bearer(self):
        def get_response(request):
            return JsonResponse({'status': 'ok'})
        
        middleware = PermissionMiddleware(get_response)
        request = HttpRequest()
        request.META = {'HTTP_AUTHORIZATION': 'test-token'}
        
        token = middleware.extract_token(request)
        assert token is None
