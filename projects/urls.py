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
]
