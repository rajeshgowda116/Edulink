from django.contrib import admin
from .models import Attendence
# Register your models here.
class Attende(admin.ModelAdmin):
    list_display = ['usn','subject_code','is_present','date','class_code']
    search_fields = ['usn','subject_code','is_present','date','class_code']

admin.site.register(Attendence, Attende)