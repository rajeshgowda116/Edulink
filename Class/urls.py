from django.urls import path
from . import views

urlpatterns = [
  path('Calculate/',views.Calculate,name='Calculate')
]