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
    if request.method == 'POST':
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
        new_user.brief_intro = '这个人很懒，什么也没写'
        new_user.avatar = 'https://miaotu-headers.oss-cn-hangzhou.aliyuncs.com/yonghutouxiang/Transparent_Akkarin.jpg'
        new_user.save()

        code = make_confirm_string(new_user)
        try:
            send_email_confirm(email, code)
        except:
            new_user.delete()
            return JsonResponse({'status_code': 6})

        return JsonResponse({'status_code': 1})
    return JsonResponse({'status_code': -1})


@csrf_exempt
def login(request):
    if request.method == 'POST':
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
    return JsonResponse({'status_code': -1})


@csrf_exempt
def change_password(request):
    if request.method == 'POST':
        username = json.loads(request.body)['username']
        old_password = json.loads(request.body)['password']
        password1 = json.loads(request.body)['password1']
        password2 = json.loads(request.body)['password2']
        try:
            user = User.objects.get(username=username)
        except:
            return JsonResponse({'status_code': 3, 'message': '没有这个用户哦'})
        if user.password == hash_code(old_password):
            if not re.match('^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,18}$', password1):
                return JsonResponse({'status_code': 4, 'message': '密码不符合规范'})
            if password1 != password2:
                return JsonResponse({'status_code': 5, 'message': '两次输入的新密码不一致'})
            user.password = hash_code(password1)
            user.save()
            return JsonResponse({'status_code': 1, 'message': '密码修改成功'})
        else:
            return JsonResponse({'status_code': 2, 'message': '密码错误!'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误'})


@csrf_exempt
def user_confirm(request):
    if request.method == 'POST':
        code = json.loads(request.body)['code']
        try:
            confirm = ConfirmString.objects.get(code=code)
        except:
            return JsonResponse({'status_code': 2})
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


@csrf_exempt
def get_userinfo(request):
    if request.method == 'POST':
        username = json.loads(request.body)['username']
        try:
            user = User.objects.get(username=username)
            return JsonResponse(
                {'status_code': 1, 'avatar': user.avatar, 'email': user.email, 'brief_intro': user.brief_intro})
        except:
            return JsonResponse({'status_code': 2, 'message': '查无此人'})
    else:
        return JsonResponse({'status_code': -1, 'message': '请求方式错误'})


@csrf_exempt
def update_avatar(request):
    if request.method == 'POST':
        username = json.loads(request.body)['username']
        avatar = json.loads(request.body)['avatar']
        try:
            user = User.objects.get(username=username)
        except:
            return JsonResponse({'status_code': 2, 'message': '查无此人!'})
        user.avatar = avatar
        user.save()
        return JsonResponse({'status_code': 1, 'message': '头像更新成功！'})
    return JsonResponse({'status_code': -1, 'message': '请求方式错误！'})
