from django.urls import path
from . import views
urlpatterns=[
  path('student_info/',views.student_info,name='student_info'),
  path('student_dashboard/',views.student_dashboard,name='student_dashboard'),
  path('student_dashboard2/',views.Student_dashbord2,name='student_dashboard2'),

]