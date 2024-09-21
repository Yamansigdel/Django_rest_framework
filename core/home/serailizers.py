from rest_framework import serializers
from .models import *

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
        fields ='__all__'


class BookSerializer(serializers.ModelSerializer):
    category=CategorySerializer() #Obtains all the foreign key from Category
    class Meta:
        model = Book
        fields ='__all__'