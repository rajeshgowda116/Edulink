from django.shortcuts import render
from Advicer.models import Classroom
# Create your views here.
def faculty_info(request):
  
  return render(request,'faculty_info.html')



  
