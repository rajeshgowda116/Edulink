from django.shortcuts import render,redirect
from User.models import User
from .models import Hod,Department
from utils.Codegen import Code
from Advicer.models import advicer, Classroom
from Faculty.models import Faculty
from Attendence.models import Attendence
from Class.models import Classes


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
  classes = Classes.objects.all()
  codes = []
  perce_detils=[]

  for clas in classes:
    codes.append({
  'class_code': clas.class_code.class_code,
  'class_name': clas.class_code.class_name,
  'subject_code': clas.subject_code.subject_code,
  'subject_name': clas.subject_code.subject_name,
   })
  for code in codes:
    total = Attendence.objects.filter(
    class_code__class_code=code['class_code'],
    subject_code__subject_code=code['subject_code']
    ).count()
    present = Attendence.objects.filter(
    class_code__class_code=code['class_code'],
    subject_code__subject_code=code['subject_code'],
    is_present=True
    ).count()
    class_name=code['class_name']
    
    if total > 0:
      percentage = (present * 100) / total
    else:
      percentage = 0
    perce_detils.append({
      'class_name':class_name,'percentage':percentage
      })
  context={'perce_detils':perce_detils}

  return render(request,'hod_attendance.html',context)





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
  faculty=User.objects.filter(role='faculty')
  faculty_row=[]
  for fac in faculty:
    faculty_info=Faculty.objects.filter(username=fac).first()
    faculty_row.append({
      'user':fac,
      'faculty_id':faculty_info.faculty_id if faculty_info else '',
      'subject_name':faculty_info.subject_name if faculty_info else ''
    })
  context={
    'faculty':faculty_row
  }
  return render(request,'faculty_list.html',context)





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
