from django.contrib import admin
from .models import Hod,Department
# Register your models here.
class HodPanal(admin.ModelAdmin):
    list_display = ['username','hod_id','mobile','college']
    search_fields = ['username','hod_id','mobile','college']

admin.site.register(Hod, HodPanal)

class DEPT(admin.ModelAdmin):
    list_display = ['username','department','dept_code']
    search_fields = ['username','department','dept_code']
admin.site.register(Department,DEPT)