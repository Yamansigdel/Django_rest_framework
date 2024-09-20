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
        return Response({'status': 403 ,'error':serializer.errors})
    
    serializer.save()
    return Response({'status':200, 'payload': serializer.data,'message':'your data is saved'})

@api_view(['PATCH'])
def update_student(request, id):
    try:
        student_objs = Student.objects.get(id=id)

        serializer = StudentSerializer(student_objs, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response({'status': 400, 'error': serializer.errors})

        serializer.save()
        return Response({'status': 200, 'payload': serializer.data, 'message': 'Update successful'})
    except Student.DoesNotExist:
        return Response({'status': 404, 'message': 'Student not found'})
    except Exception as e:
        return Response({'status': 500, 'message': str(e)})
    
@api_view(['DELETE'])
def delete_student(request, id):
    try:
        student_objs = Student.objects.get(id=id)
        student_objs.delete()
        return Response({'status':203,'message': 'deleted'})

    except Exception as e:
        print(e)
        return Response({'status':403,'message': 'invalid id'})
    
