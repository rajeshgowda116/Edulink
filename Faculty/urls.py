from django.urls import path,include
from . import views

urlpatterns = [
    path('faculty_info/',views.faculty_info,name='faculty_info'),
    path('faculty_dashboard/',views.faculty_dashboard,name='faculty_dashboard'),
    path('add_attendence/',views.add_attendence,name='add_attendence'),
    path('student_attendence/',views.student_attendence,name='student_attendence'),
    ]