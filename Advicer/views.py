from django.shortcuts import render,redirect
from utils.Codegen import Code
from .models import advicer,Classroom
from django.http import HttpResponse
from HOD.models import Department
from django.contrib.auth.decorators import login_required
from Attendence.models import Attendence
from Student.models import Student
from Faculty.models import Faculty
# Create your views here.

@login_required
def advicer_info(request):
    error = None

    if request.method == 'POST':
        advicer_id = request.POST.get('advicer_id')
        mobile_num = request.POST.get('mobile_num')
        hod_code = request.POST.get('hod_code')

        code = Department.objects.filter(dept_code=hod_code).first()

        if advicer.objects.filter(advicer_id=advicer_id).exists():
            error = "This advisor ID already exists"
        elif code:
            advicer.objects.create(
                username=request.user,
                advicer_id=advicer_id,
                mobile_num=mobile_num,
                hod_code=hod_code
            )
            return redirect("advisor_dashboard")
        else:
            error = "Your code is not Valid"

    return render(request, 'advisor_form.html', {'error': error})


@login_required
def advisor_dashboard(request):
    advisor_classrooms = Classroom.objects.filter(advisor=request.user)
    classroom = advisor_classrooms.last()

    if classroom:
        students = Student.objects.filter(
            class_code=classroom.class_code
        ).select_related('username')
    else:
        students = Student.objects.none()

    students_count = students.count()

    total_attendance = Attendence.objects.filter(
        class_code__in=advisor_classrooms
    ).count()

    present_attendance = Attendence.objects.filter(
        class_code__in=advisor_classrooms,
        is_present=True
    ).count()

    if total_attendance > 0:
        attendance_rate = round((present_attendance / total_attendance) * 100)
    else:
        attendance_rate = 0

    context = {
        'classroom': classroom,
        'students': students,
        'students_count': students_count,
        'assigned_students_count': students_count,
        'attendance_rate': attendance_rate,
        'total_attendance': total_attendance,
        'present_attendance': present_attendance,
    }

    return render(request, 'advisor_dashboard.html', context)

@login_required
def students(request):
    advisor_classrooms = Classroom.objects.filter(advisor=request.user)
    classroom = advisor_classrooms.last()

    if classroom:
        students = Student.objects.filter(
            class_code=classroom.class_code
        ).select_related('username')
    else:
        students = Student.objects.none()

    context = {
        'classroom': classroom,
        'students': students,
        'total_students': students.count(),
    }
    return render(request,'students.html', context)


def generate_class_code(request):
    classroom= Classroom.objects.filter(username=request.user).last()
    if request.method=='POST':
      class_name=request.POST.get('class')
      class_code=str(Code())
      classroom = Classroom.objects.create(username=request.user,
                                            class_name=class_name,
                                            advisor=request.user,
                                            class_code=class_code)
    context={'classroom':classroom}
    return render(request,'generate_class_code.html',context)

@login_required
def student_attendence_list(request):
   return render(request,'student_attendence.html')

@login_required
def faculty_lists(request):
    classroom = Classroom.objects.filter(advisor=request.user).last()
    code = classroom.class_code if classroom else None
    faculties = Faculty.objects.filter(class_code=code).select_related('username')
    
    context = {
        'faculty_list': faculties,
        'class_code': code
    }
        
    return render(request, 'faculty_list.html', context)
