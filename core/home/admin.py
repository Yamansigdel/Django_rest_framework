from django.contrib import admin

# Register your models here.
from home.models import *

class StudentAdmin(admin.ModelAdmin):
    list_display=('name','age','father_name')

class CategoryAdmin(admin.ModelAdmin):
    list_display=('category_name',)


class BookAdmin(admin.ModelAdmin):
    list_display=('book_title','category')



admin.site.register(Student,StudentAdmin)
admin.site.register(Book,BookAdmin)
admin.site.register(Category,CategoryAdmin)
