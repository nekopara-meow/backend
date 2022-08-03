from django.urls import path
from .views import *

urlpatterns = [
    path('establish', establish),
    path('invite', invite),
    path('setAdmins', setAdmins),
    path('deleteMem', deleteMem),
    path('view', view),
    path('viewSomeonesTeams', viewSomeonesTeams),
    # path('clear',clear),
]