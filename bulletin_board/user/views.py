import json
import bcrypt
import jwt
import re

from django.views import View
from django.http  import (
    HttpResponse,
    JsonResponse
)
from django.core.exceptions import ValidationError

from bulletin_board.settings import(
    SECRET_KEY,
    ALGORITHM
)
from .models import User

class UserSignUpView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if re.match("^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,15}$", data['password']) == None:
                return HttpResponse(status = 401)

            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            User.objects.create(
                name     = data['name'],
                password = hashed_password.decode('utf-8')
            )
            return HttpResponse(status = 200)

        except ValidationError:
            return JsonResponse({ 'message' : 'INVALID_PASSWORD'}, status = 401)

        except KeyError:
            return JsonResponse({ 'message' : 'INVALID_KEY'}, status = 400)

class UserSignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if User.objects.filter(name = data['name']).exists():
                user = User.objects.get(name = data['name'])
                print(bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')))
                
                if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                    access_token = jwt.encode({'id' : user.id}, SECRET_KEY, ALGORITHM)
                    print('-----------------------------')
                    print(access_token)
                    return JsonResponse({ 'access_token' : access_token.decode('utf-8')}, status = 200)

                return JsonResponse({ 'message' : 'UNAUTHORIZED11111111'}, status = 401)
            return JsonResponse({ 'message' : 'UNAUTHORIZED2222222222'}, status = 401)

        except KeyError:
            return JsonResponse({ 'message' : 'INVALID_KEY'}, status = 400)