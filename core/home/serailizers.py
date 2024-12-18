from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','password']
    
    #to hash the user password(by creating validation on the username and pass)
    def create(self, validated_data):
        user=User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        # field=['name','age']
        # exclude = ['id']
        fields ='__all__'

    def validate(self, data):
        if 'age' in data and data['age'] < 18:
            raise serializers.ValidationError({'error': "age cannot be less than 18"})
        
        if data['name']:
            for n in data['name']:
                if n.isdigit():
                    raise serializers.ValidationError({'error': "name can only contains letters"})


        return data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields =['category_name',]


class BookSerializer(serializers.ModelSerializer):
    category=CategorySerializer() #Obtains all the foreign key from Category
    class Meta:
        model = Book
        fields ='__all__'