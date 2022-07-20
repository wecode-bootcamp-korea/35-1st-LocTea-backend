import json, re, bcrypt, jwt

from django.http   import JsonResponse
from django.views  import View
from django.conf   import settings

from users.models import User

class SignUpView(View):
    def post(self, request):
        try:
            data           = json.loads(request.body)

            name          = data['name']
            username      = data['username']
            password      = data['password']
            mobile_number = data['mobile_number']
            birth_day     = data['birth_day']

            REGEX_ID       = '^[a-zA-Z0-9]{4,12}$'
            REGEX_PASSWORD = '^(?=.*[a-z])(?=.*\d)(?=.*[$@$!%*#?&])[a-z\d$@$!%*#?&]{8,16}$'
            REGEX_BIRTHDAY = '^(19[0-9][0-9]|20\d{2})-(0[0-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$'

            if not re.match(REGEX_ID, username):
                return JsonResponse({"message":"ID_VALIDATION_ERROR"}, status=400)

            if not re.match(REGEX_PASSWORD, password):
                return JsonResponse({"message":"PASSWORD_VALIDATION_ERROR"}, status=400)

            if not re.match(REGEX_BIRTHDAY, birth_day):
                return JsonResponse({"message":"BIRTHDAY_VALIDATION_ERROR"}, status=400)
            
            if User.objects.filter(username = username).exists():
                return JsonResponse({"message":"DUPLICATION_ERROR"}, status=400)
        
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
             name          = name,
             username      = username,
             password      = hashed_password,
             mobile_number = mobile_number,
             birth_day     = birth_day,
            )
            return JsonResponse({'message':'SUCCESS'}, status=201)
            
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

class LogInView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)

            username = data['username']
            password = data['password']

            user = User.objects.get(username = username)

            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')): 
                return JsonResponse({'message':'INVALID_USER'}, status=401)

            token = jwt.encode({"user_id":user.id}, settings.SECRET_KEY, settings.ALGORITHM)
            return JsonResponse({"message":"SUCCESS", "access_token": token}, status=200)
        
        except User.DoesNotExist:
            return JsonResponse({"message":"INVALID_USER"}, status=400)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)