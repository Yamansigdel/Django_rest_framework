from django.contrib import admin
from django.urls import path,include
from .views import *


urlpatterns = [
    
   path('excel/',ExportImportExcel.as_view()),
   path('pdf/', GeneratePdf.as_view(),name='generate_pdf'),
   path('generic-student/', StudentGeneric.as_view()),
   path('generic-student/<id>', StudentGeneric1.as_view()),
   path('student/',StudentAPI.as_view()),
   path('register/',RegisterUser.as_view()),
   # path('', home),
   # path('student/', post_student),
   # path('update-student/<id>/',update_student),
   # path('delete-student/<id>/',delete_student),
   path('get-book/',get_book),
   # path('category/',category),
]

