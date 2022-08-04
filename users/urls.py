from django.urls import path
from .views import *

urlpatterns = [
    path('login', login),
    path('register', register),
    path('confirm/email', user_confirm),
    path('get_info', get_userinfo),
    path('change_password', change_password),
    path('update/info', update_info)
]
