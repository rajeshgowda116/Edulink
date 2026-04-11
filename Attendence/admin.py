from django.contrib import admin
from .models import Attendence
# Register your models here.
class Attende(admin.ModelAdmin):
    list_display = ['usn','subject_code','is_present','date']
    search_fields = ['usn','subject_code','is_present','date']

admin.site.register(Attendence, Attende)