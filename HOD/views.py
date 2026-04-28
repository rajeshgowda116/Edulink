from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from User.models import User
from .models import Hod,Department
from utils.Codegen import Code
from Advicer.models import advicer, Classroom
from Faculty.models import Faculty
from Student.models import Student
from Attendence.models import Attendence
from Class.models import Classes
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.dateparse import parse_date


# Create your views here.
@login_required
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



@login_required
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



@login_required
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




@login_required
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




@login_required
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




@login_required
def generate_dept_code(request):
  department = Department.objects.filter(username=request.user).last()
  if request.method=='POST':
    if department:
      error = "Department code already created"
    else:
      department_name=request.POST.get('department')
      dept_code=str(Code())
      department = Department.objects.create(username=request.user,
                                             department=department_name,
                                             dept_code=dept_code)
      error = None
  else:
    error = None
  context={'department':department, 'error':error}
  return render(request,'generate_dept_code.html',context)



@login_required
def Hod_classes(request):
  hod_classes = Faculty.objects.filter(username=request.user)

  for cls in hod_classes:
    # Backfill missing class links for older faculty rows.
    classroom = Classroom.objects.filter(class_code=str(cls.class_code)).first()
    if classroom:
      Classes.objects.get_or_create(
          class_code=classroom,
          subject_code=cls,
      )

  class_links = Classes.objects.filter(subject_code__in=hod_classes)
  class_link_map = {link.subject_code_id: link.id for link in class_links}

  for cls in hod_classes:
    cls.student_count = Student.objects.filter(class_code=str(cls.class_code)).count()
    cls.class_link_id = class_link_map.get(cls.faculty_id)

  context = {
    'hod': hod_classes,
    'classes': hod_classes,
    'total_classes': hod_classes.count(),
  }
  return render(request, 'my_classes.html', context)



@login_required
def add_class(request):
    if request.method == 'POST':
        class_code = request.POST.get('class_code')
        subject_name = request.POST.get('subject_name')
        subject_code = request.POST.get('subject_code')

        user = request.user
        hod = Hod.objects.filter(username=user).first()

        if not hod:
            return HttpResponse("HOD profile not found!")

        class_code_str = str(class_code).strip()
        if not class_code_str:
            return HttpResponse("Class code is required.")
        try:
            class_code_int = int(class_code_str)
        except (TypeError, ValueError):
            return HttpResponse("Invalid class code. It must be a number.")

        faculty_key = f"{hod.hod_id}_{subject_code}"
        faculty_obj, _ = Faculty.objects.update_or_create(
            faculty_id=faculty_key,
            defaults={
                'hod': hod,
                'username': user,
                'mobile_num': hod.mobile,
                'class_code': class_code_int,
                'subject_name': subject_name,
                'subject_code': subject_code,
            }
        )

        classroom = Classroom.objects.filter(class_code=class_code_str).first()
        if not classroom:
            return HttpResponse("Classroom not found for the provided class code.")

        Classes.objects.update_or_create(
            class_code=classroom,
            subject_code=faculty_obj,
        )

        return redirect('Hod_classes')

    return render(request, 'hod_class.html')


@login_required
def add_attendence_as_Faculty(request, class_link_id=None):
  today = timezone.localdate()
  faculties = Faculty.objects.filter(username=request.user)
  class_links = Classes.objects.filter(
      subject_code__in=faculties
  ).select_related('class_code', 'subject_code')

  if class_link_id:
    class_link = get_object_or_404(class_links, id=class_link_id)
  else:
    class_link = class_links.first()

  if not class_link:
    return render(request, 'add_attendence-as-faculty.html', {
        'class': None,
        'students': [],
        'total_students': 0,
        'date': today,
        'selected_date': today,
    })

  subject = class_link.subject_code
  classroom = class_link.class_code
  selected_date = parse_date(
      request.POST.get('attendance_date') or request.GET.get('date') or ''
  ) or today

  students = Student.objects.filter(
      class_code=classroom.class_code
  ).select_related('username').order_by('usn')
  if not students.exists():
    students = Student.objects.filter(
        class_code__iexact=str(classroom.class_code).strip()
    ).select_related('username').order_by('usn')

  if request.method == 'POST':
    for student in students:
      status = request.POST.get(f'attendance_{student.id}')
      if status not in ['present', 'absent']:
        continue

      Attendence.objects.update_or_create(
          usn=student,
          subject_code=subject,
          class_code=classroom,
          date=selected_date,
          defaults={'is_present': status == 'present'},
      )

    return redirect('add_attendence_as_Faculty', class_link_id=class_link.id)

  attendance_by_student = {
      attendance.usn_id: attendance
      for attendance in Attendence.objects.filter(
          subject_code=subject,
          class_code=classroom,
          date=selected_date,
      )
  }

  student_rows = []
  for student in students:
    attendance = attendance_by_student.get(student.id)
    today_status = ''
    if attendance:
      today_status = 'present' if attendance.is_present else 'absent'

    student_rows.append({
        'id': student.id,
        'first_name': student.username.first_name if student.username else '',
        'last_name': student.username.last_name if student.username else '',
        'student_id': student.usn,
        'today_status': today_status,
    })

  context = {
      'class': {
          'id': class_link.id,
          'name': subject.subject_name,
          'code': subject.subject_code,
          'class_name': classroom.class_name,
          'class_code': classroom.class_code,
      },
      'students': student_rows,
      'total_students': len(student_rows),
      'date': selected_date,
      'selected_date': selected_date,
  }

  return render(request, 'add_attendence-as-faculty.html', context)





@login_required
def Chat(request):
  return render(request,'chat.html')

