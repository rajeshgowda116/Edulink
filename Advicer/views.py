from django.shortcuts import render,redirect
from utils.Codegen import Code
from .models import advicer,Classroom
from django.http import HttpResponse
from HOD.models import Department
from django.contrib.auth.decorators import login_required
from Attendence.models import Attendence
from Student.models import Student
from Faculty.models import Faculty
from Class.models import Classes
import json
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
    classroom = Classroom.objects.filter(advisor=request.user).last()

    if not classroom:
        context = {
            'classroom': None,
            'subjects': [],
            'students_json': '[]',
            'subjects_json': '[]',
        }
        return render(request, 'student_attendence.html', context)

    class_links = Classes.objects.filter(class_code=classroom).select_related('subject_code')
    subjects = [link.subject_code for link in class_links if link.subject_code]

    students = Student.objects.filter(
        class_code=classroom.class_code
    ).select_related('username').order_by('usn')

    if not students.exists():
        students = Student.objects.filter(
            class_code__iexact=str(classroom.class_code).strip()
        ).select_related('username').order_by('usn')

    students_payload = []
    for student in students:
        full_name = " ".join(
            x for x in [
                student.username.first_name if student.username else '',
                student.username.last_name if student.username else '',
            ] if x
        ) or student.usn

        row = {
            'name': full_name,
            'usn': student.usn,
            'scores': {},
        }

        for subject in subjects:
            total = Attendence.objects.filter(
                usn=student,
                class_code=classroom,
                subject_code=subject
            ).count()
            present = Attendence.objects.filter(
                usn=student,
                class_code=classroom,
                subject_code=subject,
                is_present=True
            ).count()

            percentage = round((present / total) * 100) if total else 0
            row['scores'][subject.subject_code] = percentage

        students_payload.append(row)

    subjects_payload = [
        {
            'code': subject.subject_code,
            'name': subject.subject_name or subject.subject_code
        }
        for subject in subjects
    ]

    context = {
        'classroom': classroom,
        'subjects': subjects_payload,
        'students_json': json.dumps(students_payload),
        'subjects_json': json.dumps(subjects_payload),
    }
    return render(request, 'student_attendence.html', context)

@login_required
def faculty_lists_advicer(request):
    classroom = Classroom.objects.filter(advisor=request.user).last()
    code = classroom.class_code if classroom else None
    class_name = classroom.class_name if classroom else "N/A"
    
    faculties = Faculty.objects.filter(class_code=code).select_related('username')
    total_faculty = faculties.count()
    
    department_name = "N/A"
    adv = advicer.objects.filter(username=request.user).first()
    if adv:
        dept = Department.objects.filter(dept_code=adv.hod_code).first()
        if dept:
            department_name = dept.department

    context = {
        'faculty_list': faculties,
        'class_code': code,
        'class_name': class_name,
        'total_faculty': total_faculty,
        'department': department_name,
    }
        
    return render(request, 'advisor_faculty_list.html', context)
