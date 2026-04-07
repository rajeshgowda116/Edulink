from django.contrib import admin
from .models import Faculty
# Register your models here.
class faculty(admin.ModelAdmin):
    list_display = ['username','faculty_id','mobile_num','class_code']
    search_fields = ['username','faculty_id','mobile_num','class_code']

admin.site.register(Faculty, faculty)