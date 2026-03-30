from django.contrib import admin
from .models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'role']
    search_fields = ['first_name', 'last_name', 'email', 'role']

admin.site.register(User, UserAdmin)
