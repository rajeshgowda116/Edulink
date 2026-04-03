from django.shortcuts import render
from User.models import User

# Create your views here.
def hod_dashboard(request):
  return render(request,'hod_dashboard.html')

def class_attendence(request):
  return render(request,'hod_attendance.html')

def advicers_list(request):
  user= User.objects.filter
  context={'user':user}
  return render(request,'advisors_list.html',context)

def faculty_list(request):
  return render(request,'faculty_list.html')

def generate_dept_code(request):
  return render(request,'generate_class_code.html')

def Chat(request):
  return render(request,'chat.html')
