from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serailizers import * 

@api_view(['GET'])
def home(request):
    student_objs=Student.objects.all()
    serializer=StudentSerializer(student_objs,many=True)
    return Response({'status': 200, 'payload': serializer.data})

@api_view(['POST'])
def post_student(request):

    serializer=StudentSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response({'status': 403 ,'message':'something went wrong'})
    
    serializer.save()
    return Response({'status':200, 'payload': serializer.data,'message':'you send'})
