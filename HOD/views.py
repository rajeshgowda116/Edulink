from django.shortcuts import render,redirect
from User.models import User
from .models import Hod,Department
from utils.Codegen import Code
from Advicer.models import advicer, Classroom


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
  advisors_count = User.objects.filter(role='advisor').count()
  faculty_count=User.objects.filter(role='faculty').count()
  students_count=User.objects.filter(role='student').count()
  department=Department.objects.filter(username=request.user).first()
  context={'advisors_count': advisors_count,
           'faculty_count':faculty_count,
           'students_count':students_count,
           'department':department}
  
  return render(request,'hod_dashboard.html',context)

def class_attendence(request):
  return render(request,'hod_attendance.html')

def advicers_list(request):
  advisors= User.objects.filter(role='advisor')
  advisor_rows = []
  for advisor in advisors:
    advicer_info = advicer.objects.filter(username=advisor).first()
    classroom = Classroom.objects.filter(advisor=advisor).first()
    advisor_rows.append({
      'user': advisor,
      'advicer_id': advicer_info.advicer_id if advicer_info else '',
      'class_name': classroom.class_name if classroom else '',
    })
  context={'advisors':advisor_rows}
  return render(request,'advisors_list.html',context)

def faculty_list(request):
  return render(request,'faculty_list.html')

def generate_dept_code(request):
  department = Department.objects.filter(username=request.user).last()
  if request.method=='POST':
    department_name=request.POST.get('department')
    dept_code=Code()
    department = Department.objects.create(username=request.user,
                                           department=department_name,
                                           dept_code=dept_code)
  context={'department':department}
  return render(request,'generate_class_code.html',context)

def Chat(request):
  return render(request,'chat.html')
