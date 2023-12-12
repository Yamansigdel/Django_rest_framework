from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def home(request):
    if request.method=='GET':
        return Response({'status': 200, 'message': 'Hello from django_rest_framework'})

