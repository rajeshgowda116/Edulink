from django.urls import path
from . import views
urlpatterns = [
  path('hod_dashboard/',views.hod_dashboard,name='hod_dashboard'),
  path('claa_attendence/',views.class_attendence,name='class_attendence'),
  path('advicers_list/',views.advicers_list,name='advicers_list'),
  path('faculty_list/',views.faculty_list,name='faculty_list'),
  path('generate_dept_code/',views.generate_dept_code,name='generate_dept_code'),
  path('Chat/',views.Chat,name='Chat')
]