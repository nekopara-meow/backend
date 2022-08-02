# Create your views here.
import json
import re

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pytz import utc

from users.models import User
from utils.email import *
from utils.token import create_token
from utils.token import check_token


@csrf_exempt
def register(request):
    username = json.loads(request.body)['username']
    password1 = json.loads(request.body)['password1']
    password2 = json.loads(request.body)['password2']
    email = json.loads(request.body)['email']

    same_name_user = User.objects.filter(username=username)
    if same_name_user:
        return JsonResponse({'status_code': 2})

    same_email_user = User.objects.filter(email=email)
    if same_email_user:
        return JsonResponse({'status_code': 3})

        # 检测密码不符合规范：8-18，英文字母+数字
    if not re.match('^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,18}$', password1):
        return JsonResponse({'status_code': 4})

    if password1 != password2:
        return JsonResponse({'status_code': 5})

    # success
    new_user = User()
    new_user.username = username
    new_user.password = hash_code(password1)
    new_user.email = email
    new_user.save()

    code = make_confirm_string(new_user)
    try:
        send_email_confirm(email, code)
    except:
        new_user.delete()
        return JsonResponse({'status_code': 6})

    return JsonResponse({'status_code': 1})


@csrf_exempt
def login(request):
    username = request.META.get('HTTP_USERNAME')
    token = request.META.get('HTTP_AUTHORIZATION')
    if username is not None and token is not None and check_token(username, token):
        return JsonResponse({'status_code': 2})

    username = json.loads(request.body)['username']
    password = json.loads(request.body)['password']
    try:
        user = User.objects.get(username=username)
    except:
        return JsonResponse({'status_code': 3})

    if user.password == hash_code(password):
        if not user.has_confirmed:
            return JsonResponse({'status_code': 5})
        token = create_token(username)
        return JsonResponse({'status_code': 1, 'username': username, 'token': token})
    else:
        return JsonResponse({'status_code': 4})


@csrf_exempt
def user_confirm(request):
    if request.method == 'POST':
        code = json.loads(request.body)['code']
        try:
            confirm = ConfirmString.objects.get(code=code)
        except:
           return JsonResponse({'status_code':2})
        c_time = confirm.c_time.replace(tzinfo=utc)
        now = datetime.datetime.now().replace(tzinfo=utc)
        if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
            confirm.user.delete()
            return JsonResponse({'status_code': 3})
        else:
            confirm.user.has_confirmed = True
            confirm.user.save()
            confirm.delete()
            return JsonResponse({'status_code': 1})
    return JsonResponse({'status_code': -1})
