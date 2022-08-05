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
    path('delete/xml', deleteXML),
    path('delete/doc', deleteDOC)
]
