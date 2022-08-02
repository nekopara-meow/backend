from django.urls import path
from .views import *

urlpatterns = [
    path('login', login),
    path('register', register),
    path('confirm/email', user_confirm),
]