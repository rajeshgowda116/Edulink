from django.shortcuts import render
from Advicer.models import Classroom
# Create your views here.
def create_classroom(request):
  if request.method=='POST':
    code=request.POST.get()
    class_name=request.POST.get()
    if code==Classroom.code:
      print("hi")



  
