from django.urls import path
from .views import *

urlpatterns = [
    path('establish', establish),
    path('invite', invite),
    path('setAdmins', setAdmins),
    path('deleteMem', deleteMem),
    path('viewMembersInTeam', viewMembersInTeam),
    path('viewSomeonesTeams0', viewSomeonesTeams0),
    path('viewSomeonesTeams1', viewSomeonesTeams1),
    path('viewSomeonesTeams2', viewSomeonesTeams2),
    path('viewTeam', viewTeam),

    path('uml/save', save_uml),
    path('uml/load', load_uml)
]
