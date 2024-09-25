from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serailizers import * 
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token


from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['GET'])
def get_book(request):
    book_objs=Book.objects.all()
    serializer=BookSerializer(book_objs,many=True)  
    return Response({'status': 200, 'payload': serializer.data})

class RegisterUser(APIView):

    def post(self, request):
        serializer=UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'status': 403 ,'error':serializer.errors})
        
        serializer.save()

        user=User.objects.get(username=serializer.data['username'])
        #token_obj , _ = Token.objects.get_or_create(user=user)  #token_auth method
        refresh = RefreshToken.for_user(user)   #jwt token method
        
        #return Response({'status':200, 'payload': serializer.data,'token':str(token_obj),'message':'your data is saved'})
        return Response({'status':200, 'payload': serializer.data,'refresh': str(refresh),
        'access': str(refresh.access_token),'message':'your data is saved'})
       
        


# from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication   

class StudentAPI(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get (self, request):
        student_objs=Student.objects.all()
        serializer=StudentSerializer(student_objs,many=True)
        print(request.user)
        return Response({'status': 200, 'payload': serializer.data})

    def post (self, request):

        serializer=StudentSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'status': 403 ,'error':serializer.errors})
        
        serializer.save()
        return Response({'status':200, 'payload': serializer.data,'message':'your data is saved'})
    

    def put (self, request):

        try:
            student_objs = Student.objects.get(id=request.data['id'])

            serializer = StudentSerializer(student_objs, data=request.data)

            if not serializer.is_valid():
                return Response({'status': 400, 'error': serializer.errors})

            serializer.save()
            return Response({'status': 200, 'payload': serializer.data, 'message': 'Update successful'})
        except Student.DoesNotExist:
            return Response({'status': 404, 'message': 'Student not found'})
        except Exception as e:
            return Response({'status': 500, 'message': str(e)})

    def patch (self, request):
 
        try:
            student_objs = Student.objects.get(id=request.data['id'])

            serializer = StudentSerializer(student_objs, data=request.data, partial=True)

            if not serializer.is_valid():
                return Response({'status': 400, 'error': serializer.errors})

            serializer.save()
            return Response({'status': 200, 'payload': serializer.data, 'message': 'Update successful'})
        except Student.DoesNotExist:
            return Response({'status': 404, 'message': 'Student not found'})
        except Exception as e:
            return Response({'status': 500, 'message': str(e)})       

    def delete (self, request):
        try:
            student_objs = Student.objects.get(id=request.data['id'])
            student_objs.delete()
            return Response({'status':203,'message': 'deleted'})

        except Exception as e:
            print(e)
            return Response({'status':403,'message': 'invalid id'})













# @api_view(['GET'])
# def category(request):
#     category_objs=Category.objects.all()
#     serializer=CategorySerializer(category_objs,many=True)  
#     return Response({'status': 200, 'payload': serializer.data})


# @api_view(['GET'])
# def home(request):
#     student_objs=Student.objects.all()
#     serializer=StudentSerializer(student_objs,many=True)
#     return Response({'status': 200, 'payload': serializer.data})

# @api_view(['POST'])
# def post_student(request):

#     serializer=StudentSerializer(data=request.data)

#     if not serializer.is_valid():
#         return Response({'status': 403 ,'error':serializer.errors})
    
#     serializer.save()
#     return Response({'status':200, 'payload': serializer.data,'message':'your data is saved'})

# @api_view(['PUT'])
# def update_student(request, id):
#     try:
#         student_objs = Student.objects.get(id=id)

#         serializer = StudentSerializer(student_objs, data=request.data)

#         if not serializer.is_valid():
#             return Response({'status': 400, 'error': serializer.errors})

#         serializer.save()
#         return Response({'status': 200, 'payload': serializer.data, 'message': 'Update successful'})
#     except Student.DoesNotExist:
#         return Response({'status': 404, 'message': 'Student not found'})
#     except Exception as e:
#         return Response({'status': 500, 'message': str(e)})
    
# @api_view(['DELETE'])
# def delete_student(request, id):
#     try:
#         student_objs = Student.objects.get(id=id)
#         student_objs.delete()
#         return Response({'status':203,'message': 'deleted'})

#     except Exception as e:
#         print(e)
#         return Response({'status':403,'message': 'invalid id'})
    
from rest_framework import generics


class StudentGeneric(generics.ListAPIView,generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentGeneric1(generics.UpdateAPIView,generics.DestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field='id'


from .helpers import save_pdf
import datetime

class GeneratePdf(APIView):
    def get(self, request):
            student_objs=Student.objects.all()
            params ={
                'today': datetime.date.today(),
                'student_objs': student_objs
            }
            file_name, status = save_pdf(params)
            print(status)


            if not status: 
                return Response({'status': 400})


            return Response({'status': 200, 'path' :  f'\media\{file_name}.pdf'})
    
import pandas as pd
from django.conf import settings
import uuid

class ExportImportExcel(APIView):
    def get(self,request):
        student_objs=Student.objects.all()
        serializer=StudentSerializer(student_objs,many=True)
        df=pd.DataFrame(serializer.data)
        df.to_csv(f"public/static/excel/{uuid.uuid4()}.csv", encoding="UTF-8",index=False)
        print(df)

        return Response({'status': 200})

    def post(self,request):
        #exceled_upload_obj=ExcelFileUpload.objects.create(excel_file_upload=request.FILES['files']) #relative path of file
        #df= pd.read_csv(f"{settings.BASEDIR}/public/static/{exceled_upload_obj.excel_file_upload}") #concatenated with base dir
        exceled_upload_obj=ExcelFileUpload.objects.first()
        file_path = exceled_upload_obj.excel_file_upload.path #(alternative)(fullpath)
        df=pd.read_csv(file_path)
        print(df)
        for student in(df.values.tolist()):
            Student.objects.create(
                name=student[1],
                age=student[2],
                father_name=student[3]
            )


        return Response({'status': 200})