from django.contrib import admin
from marks.models import Marks

# Register your models here.
class marks(admin.ModelAdmin):
    list_display = ['student','subject','internal1','internal2']
    search_fields =['student','subject']

admin.site.register(Marks, marks)
