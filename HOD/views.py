from django.shortcuts import render,redirect
from User.models import User
from .models import Hod

# Create your views here.
def hod_info(request):
  if request.method=='POST':
    hod_id=request.POST.get('hod_id')
    mobile=request.POST.get('mobile')
    college=request.POST.get('college')
    Hod.objects.create(
        username=request.user,
        hod_id=hod_id,
        mobile=mobile,
        college=college
        )
    return redirect("hod_dashboard")
  return render(request,'hod_info.html')

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
