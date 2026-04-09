from django.contrib import admin
from .models import Student
# Register your models here.
class student(admin.ModelAdmin):
    list_display = ['username','usn','mobile_num','class_code']
    search_fields = ['username','usn','mobile_num','class_code']

admin.site.register(Student, student)