from django.contrib import admin
from .models import Classes
# Register your models here.
class Class(admin.ModelAdmin):
    list_display = ['subject_code','class_code']
    search_fields = ['subject_code','class_code']

admin.site.register(Classes, Class)