from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from Advicer.models import Classroom
from Attendence.models import Attendence
from .models import Student
# Create your views here.
@login_required
def student_info(request):
  if request.method=='POST':
    usn=request.POST.get('usn')
    mobile_num=request.POST.get('mobile_num')
    class_code=request.POST.get('class_code')
    Student.objects.create(username=request.user,
                           usn=usn,
                           mobile_num=mobile_num,
                           class_code=class_code)
    return redirect('student_dashboard')

  return render(request,'student_info.html')

@login_required
def student_dashboard(request):
    student = Student.objects.filter(username=request.user).first()

    if not student:
        context = {
            'student': None,
            'classes': [],
            'today_schedule': [],
            'total_classes': 0,
            'attendance_pct': 0,
            'total_attendance': 0,
            'present_attendance': 0,
        }
        return render(request, 'student_dashboard.html', context)

    attendance = Attendence.objects.filter(usn=student)
    classrooms = Classroom.objects.filter(class_code=student.class_code)

    total = attendance.count()
    present = attendance.filter(is_present=True).count()

    if total > 0:
        attendance_pct = round((present / total) * 100)
    else:
        attendance_pct = 0

    classes = []

    for classroom in classrooms:
        class_att = attendance.filter(class_code=classroom)
        class_total = class_att.count()
        class_present = class_att.filter(is_present=True).count()

        if class_total > 0:
            class_pct = round((class_present / class_total) * 100)
        else:
            class_pct = 0

        classes.append({
            'class_name': classroom.class_name,
            'class_code': classroom.class_code,
            'attendance_pct': class_pct,
            'present': class_present,
            'total': class_total,
        })

    context = {
        'student': student,
        'classes': classes,
        'today_schedule': classes,
        'total_classes': len(classes),
        'attendance_pct': attendance_pct,
        'total_attendance': total,
        'present_attendance': present,
    }

    return render(request, 'student_dashboard.html', context)
