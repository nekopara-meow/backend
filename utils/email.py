from django.conf import settings

from users.models import ConfirmString
from utils.hash import *

import datetime


def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.username, now)
    ConfirmString.objects.create(code=code, user=user, )
    return code


def send_email_confirm(email, code):
    from django.core.mail import EmailMultiAlternatives

    subject = '来自喵途论坛的注册确认邮件'

    text_content = '''感谢您的注册，这里是喵途论坛，专注于计算机系同学学习生活！\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''
    html_content = '''
                       <p>感谢注册<a href="{}/confirm?code={}" target=blank>喵途论坛</a>，\
                       这里是喵途论坛，专注于计算机系同学学习生活！</p>
                       <p>请点击站点链接完成注册确认！</p>
                       <p>此链接有效期为{}天！</p>
                       '''.format(settings.FRONTEND, code, settings.CONFIRM_DAYS)  # url must be corrected
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
