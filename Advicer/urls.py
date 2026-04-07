from django.urls import path,include
from . import views

urlpatterns = [
    path('advicer_info/',views.advicer_info,name='advicer_info'),
    path('advisor_dashboard/',views.advisor_dashboard,name='advisor_dashboard'),
    ]