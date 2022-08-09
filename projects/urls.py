from django.urls import path
from .views import *

urlpatterns = [
    path('establish', establish),
    path('delete', delete),
    path('rename', rename),
    path('uploadFile', uploadFile),
    path('viewFilesInProject', viewFilesInProject),
    path('viewUMLsInProject', viewUMLsInProject),
    path('viewDesignsInProject', viewDesignsInProject),
    path('viewTextsInProject', viewTextsInProject),
    path('clear', clear),
    path('load/xml', loadXML),
    path('load/doc', loadDOC),
    path('new/xml', newXML),
    path('new/doc', newDOC),
    path('save/xml', saveXML),
    path('save/doc', saveDOC),
    path('delete/file', del_file_by_id),
    path('rename/file', rename_file_by_id),
    path('getfiles/byproject', get_files_by_project),
    path('getfiles/byuser',get_files_by_user),
    path('getfiles/bycreator',get_files_by_creator),
    path('getprojects/byuser',get_projects_by_user)
]
