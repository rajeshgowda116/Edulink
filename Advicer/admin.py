from django.contrib import admin
from .models import advicer,Classroom

# Register your models here.
class Advicer(admin.ModelAdmin):
    list_display = ['username','advicer_id','mobile_num','hod_code']
    search_fields = ['username','advicer_id','mobile_num','hod_code']

admin.site.register(advicer, Advicer)

class classroom(admin.ModelAdmin):
    list_display = ['username','class_name','class_code']
    search_fields = ['username','class_name','class_code']

admin.site.register(Classroom, classroom)

