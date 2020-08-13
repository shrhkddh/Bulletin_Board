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

from bulletin_board.settings import (
    SECRET_KEY,
    ALGORITHM
)
from .models import Board

class BoardView(View):
    def post(self, request):
        data = json.loads(request.body)
        x_forwardede_for = request.META.get('HTTP_X_FORWARDED_FOR')

        try:
            
            if x_forwardede_for:
                ip = x_forwardede_for.split(',')[0]

            else:
                ip = request.META.get('REMOTE_ADDR')

            if re.match("^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,15}$", data['password']) == None:
                return JsonResponse( {'message' : 'INVALID_PASSWORD'}, status = 401)

            hashed_password = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())

            Board.objects.create(
                name        = data['name'],
                password    = hashed_password.decode(),
                title       = data['title'],
                description = data['description'],
                user_ip     = ip
            )
            return HttpResponse(status = 200)

        except KeyError:
            return JsonResponse( {'message' : 'INVALID_KEY'}, status = 400)

    def get(self, request):
        board_detail = Board.objects.values()

        if board_detail:
            return JsonResponse( {'Board' : list(board_detail[::-1])}, status = 200)
        return JsonResponse( {'message' : 'No Posts.'}, status = 200)

    def patch(self, request):
        data = json.loads(request.body)

        try:
            if Board.objects.filter(name = data['name']).exists():
                user = Board.objects.get(name = data['name'])

                if bcrypt.checkpw(data['password'].encode(), user.password.encode()):

                    Board.objects.filter(name = user.name).update(
                        title       = data['title'],
                        description = data['description']
                    )
                    return HttpResponse(status = 200)

                return JsonResponse( {'message' : 'UNAUTHORIZED PW'}, status = 401)
            return JsonResponse( {'message' : 'UNAUTHORIZED ID'}, status = 401)
        
        except KeyError:
            return JsonResponse( {'message' : 'INVALID_KEY'}, status = 400)

    def delete(self, request):
        data = json.loads(request.body)
        try:

            if Board.objects.filter(name = data['name']).exists():
                user = Board.objects.get(name = data['name'])

                if bcrypt.checkpw(data['password'].encode(), user.password.encode()):

                    Board.objects.filter(name = user.name).delete()

                    return HttpResponse(status = 200)

                return JsonResponse( {'message' : 'UNAUTHORIZED PW'}, status = 401)
            return JsonResponse( {'message' : 'UNAUTHORIZED ID'}, status = 401)
            
        except KeyError:
            return JsonResponse( {'message' : 'INVALID_KEY'}, status = 400)

class BoardListView(View):
    def get(self, request):
        board_list = Board.objects.all()

        if board_list: 
            BoardList = [{
                "postNum"   : i.id,
                "postTitle" : i.title,
                "postDate"  : i.updated_at,
                "userIp"    : i.user_ip
            }for i in board_list]

            return JsonResponse( {'BoardList' : BoardList[::-1]}, status = 200)
        return JsonResponse( {'message' : 'No List.'}, status = 200)