from django.urls import path,include
from . import views

urlpatterns = [
    path('advicer_info/',views.advicer_info,name='advicer_info'),
    path('advisor_dashboard/',views.advisor_dashboard,name='advisor_dashboard'),
    path('students/',views.students,name='students'),
    path('generate_class_code',views.generate_class_code,name='generate_class_code'),
    path('student_attendence_list/',views.student_attendence_list,name='student_attendence_list'),
    path('faculty_lists_advicer/',views.faculty_lists_advicer,name='faculty_lists_advicer'),
    path('advicer_class/',views.advicer_class,name='advicer_class'),
    path('advicer_add_attendence/<int:class_link_id>/',views.advicer_add_attendence,name='advicer_add_attendence'),
    path('advicer_student_attendence_list/<int:class_link_id>/',views.advicer_student_attendence_list,name='advicer_student_attendence_list'),
    path('add_marks_asadvisor/<int:class_link_id>/', views.add_marks_asadvisor, name='add_marks_asadvisor'),

    path('show_marks/<int:class_link_id>/', views.show_marks, name='show_marks'),
    path('advicer_class_add/', views.advicer_class_add, name='advicer_class_add'),
    path('streak_maintainer/<int:class_link_id>/', views.streak_maintainer, name='advicer_streak_maintainer'),
    ]
