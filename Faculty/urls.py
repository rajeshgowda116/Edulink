from django.urls import path,include
from . import views

urlpatterns = [
    path('faculty_info/',views.faculty_info,name='faculty_info'),
    ]