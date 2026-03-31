from django.urls import path
from . import views
urlpatterns = [
  path('hod_dashboard',views.hod_dashboard,name='hod_dashboard')
]