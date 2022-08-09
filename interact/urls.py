from django.urls import path
from .views import *

urlpatterns = [
    path('getPersonalMessage', getPersonalMessage),
    path('getTeamMessage', getTeamMessage),
    path('getProjectMessage', getProjectMessage),
    path('agreeInvitation', agreeInvitation),
    path('disagreeInvitation', disagreeInvitation),


    # path('getPersonalMessage', getPersonalMessage),
    # path('getPersonalMessage', getPersonalMessage),
    # path('getPersonalMessage', getPersonalMessage),
    # path('getPersonalMessage', getPersonalMessage),
    # path('getPersonalMessage', getPersonalMessage),

]