from django.urls import path,include
from . import views

urlpatterns = [
    path('faculty_info/',views.faculty_info,name='faculty_info'),
    path('faculty_dashboard/',views.faculty_dashboard,name='faculty_dashboard'),
    path('add_attendence/',views.add_attendence,name='add_attendence'),
    path('add_attendence/<int:class_link_id>/',views.add_attendence,name='add_attendence'),
    path('student_attendence/',views.student_attendence,name='student_attendence'),
    path('student_list/',views.student_list,name='student_list'),
    path('student_list/<int:class_link_id>/',views.student_list,name='student_list'),
    path('add_class_as_faculty/',views.add_class_as_faculty,name='add_class_as_faculty'),
    path('add_marks/',views.add_marks,name='add_marks'),
    path('add_marks/<int:class_link_id>/',views.add_marks,name='add_marks'),
    path('show_marks/',views.show_marks,name='show_marks'),
    path('show_marks/<int:class_link_id>/',views.show_marks,name='show_marks'),
    ]
