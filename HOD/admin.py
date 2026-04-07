from django.contrib import admin
from .models import Hod
# Register your models here.
class HodPanal(admin.ModelAdmin):
    list_display = ['username','hod_id','mobile','college']
    search_fields = ['username','hod_id','mobile','college']

admin.site.register(Hod, HodPanal)