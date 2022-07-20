import json

import jwt

from django.http        import JsonResponse
from users.models       import User
from django.conf        import settings

def LoginDecorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            if 'Authorization' not in request.headers:
                return JsonResponse({'message' : 'NO_PERMISSION'}, status = 401)

            access_token = request.headers.get('Authorization')
            payload      = jwt.decode(access_token, settings.SECRET_KEY, settings.ALGORITHM)
            user_id      = payload['id']

            if not User.objects.filter(id = user_id).exists():
                return JsonResponse({ 'message' : 'INVALID_USER' }, status = 401)
        
            user         = User.objects.get(id = user_id)
            request.user = user

            return func(self, request, *args, **kwargs)

        except jwt.exceptions.DecodeError:
            return JsonResponse({ 'message' : 'INVALID_TOKEN' }, status = 400)
        
        except KeyError:
            return JsonResponse({ 'message' : 'KEY_ERROR' }, status = 400)

    return wrapper