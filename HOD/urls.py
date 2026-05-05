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
  path('add_attendence_as_faculty/', views.add_attendence_as_Faculty, name='add_attendence_as_Faculty'),
  path('add_attendence_as_faculty/<int:class_link_id>/', views.add_attendence_as_Faculty, name='add_attendence_as_Faculty'),
  path('student_list_hod/',views.student_list_hod,name='student_list_hod'),
  path('student_list_hod/<int:class_link_id>/',views.student_list_hod,name='student_list_hod'),
  path('Chat/',views.Chat,name='Chat'),
  path('hod_add_marks/', views.hod_add_marks, name='hod_add_marks'),
  path('hod_add_marks/<int:class_link_id>/', views.hod_add_marks, name='hod_add_marks'),
  path('hod_show_marks/', views.hod_show_marks, name='hod_show_marks'),
  path('hod_show_marks/<int:class_link_id>/', views.hod_show_marks, name='hod_show_marks'),
  path('hod_streak_maintainer/', views.hod_streak_maintainer, name='hod_streak_maintainer'),
  path('hod_streak_maintainer/<int:class_link_id>/', views.hod_streak_maintainer, name='hod_streak_maintainer'),
]

