from django.contrib import admin

# Register your models here.
from home.models import Student

class StudentAdmin(admin.ModelAdmin):
    list_display=('name','age','father_name')

admin.site.register(Student,StudentAdmin)