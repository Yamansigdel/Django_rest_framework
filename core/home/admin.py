from django.contrib import admin

# Register your models here.
from home.models import *

class StudentAdmin(admin.ModelAdmin):
    list_display=('name','age','father_name')

class CategoryAdmin(admin.ModelAdmin):
    list_display=('category_name',)


class BookAdmin(admin.ModelAdmin):
    list_display=('book_title','category')

class ExcelFileUploadAdmin(admin.ModelAdmin):
    list_display=('excel_file_upload',)


admin.site.register(Student,StudentAdmin)
admin.site.register(Book,BookAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(ExcelFileUpload,ExcelFileUploadAdmin)