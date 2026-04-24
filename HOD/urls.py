from django.urls import path
from . import views
urlpatterns = [
  path('hod_info/',views.hod_info,name='hod_info'),
  path('hod_dashboard/',views.hod_dashboard,name='hod_dashboard'),
  path('claa_attendence/',views.class_attendence,name='class_attendence'),
  path('advicers_list/',views.advicers_list,name='advicers_list'),
  path('faculty_list/',views.faculty_list,name='faculty_list'),
  path('generate_dept_code/',views.generate_dept_code,name='generate_dept_code'),
  path('Hod_classes/',views.Hod_classes,name='Hod_classes'),
  path('add_class/',views.add_class,name='add_class'),
  path('Chat/',views.Chat,name='Chat')
]
