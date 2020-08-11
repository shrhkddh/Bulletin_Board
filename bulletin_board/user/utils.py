import jwt
import json

from django.http import JsonResponse, HttpResponse

from bulletin_board.settings import SECRET_KEY, ALGORITHM
from .models import User

def login_required(func):
    def wrapper(self, request, *args, **kwargs):

        try:
            access_token = request.headers['Authorization']
            user_id      = jwt.decode(access_token, SECRET_KEY, ALGORITHM)['id']
            user         = User.objects.get(id = user_id)
            request.user = user

            return func(self, request, *args, **kwargs)
        
        except KeyError:
            return HttpResponse(status = 400)

        except User.DoesNotExist:
            return JsonResponse({ 'message' : 'UNKNOWN_USER' }, status = 401)

        except json.decoder.JSONDecodeError:
            return JsonResponse({ 'message' : 'INVALID_TOKEN' }, status = 401)

    return wrapper