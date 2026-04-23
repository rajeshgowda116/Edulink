from django.urls import path,include
from . import views

urlpatterns = [
    path('advicer_info/',views.advicer_info,name='advicer_info'),
    path('advisor_dashboard/',views.advisor_dashboard,name='advisor_dashboard'),
    path('students/',views.students,name='students'),
    path('generate_class_code',views.generate_class_code,name='generate_class_code'),
    path('student_attendence_list/',views.student_attendence_list,name='student_attendence_list'),
    path('faculty_lists_advicer/',views.faculty_lists_advicer,name='faculty_lists_advicer'),
    ]