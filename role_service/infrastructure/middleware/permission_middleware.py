import jwt
from django.conf import settings
from django.http import JsonResponse


class PermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_paths = [
            '/api/role/health/',
            '/api/role/events/',
            '/api/role/organizations/',
            '/admin/'
        ]
    
    def __call__(self, request):
        if any(request.path.startswith(path) for path in self.exempt_paths):
            return self.get_response(request)
        
        if hasattr(self.get_response, 'view_class'):
            view_class = self.get_response.view_class
            if hasattr(view_class, 'permission_classes'):
                from rest_framework.permissions import AllowAny
                if AllowAny in view_class.permission_classes:
                    return self.get_response(request)
        
        token = self.extract_token(request)
        if not token:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            request.user_id = payload.get('user_id')
            request.session_id = payload.get('session_id')
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Token expired'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Invalid token'}, status=401)
        
        return self.get_response(request)
    
    def extract_token(self, request):
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            return auth_header[7:]
        return None
