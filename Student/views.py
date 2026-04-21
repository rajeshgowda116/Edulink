from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
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
  student_profiles = Student.objects.filter(username=request.user)
  class_codes = student_profiles.values_list('class_code', flat=True).distinct()

  attendance = Attendence.objects.filter(usn__in=student_profiles)
  attendance_classroom_ids = attendance.exclude(class_code__isnull=True).values_list(
    'class_code_id',
    flat=True
  ).distinct()
  classrooms = Classroom.objects.filter(
    Q(class_code__in=class_codes) | Q(id__in=attendance_classroom_ids)
  ).distinct()

  attendance_summary = attendance.aggregate(
    total=Count('id'),
    present=Count('id', filter=Q(is_present=True)),
  )

  total_attendance = attendance_summary['total'] or 0
  present_attendance = attendance_summary['present'] or 0
  attendance_pct = round((present_attendance / total_attendance) * 100) if total_attendance else 0

  class_attendance = {
    item['class_code__class_code']: item
    for item in attendance.values('class_code__class_code').annotate(
      total=Count('id'),
      present=Count('id', filter=Q(is_present=True)),
    )
  }

  classes = []
  for classroom in classrooms:
    summary = class_attendance.get(classroom.class_code, {})
    class_total = summary.get('total', 0) or 0
    class_present = summary.get('present', 0) or 0
    class_pct = round((class_present / class_total) * 100) if class_total else 0
    classes.append({
      'class_name': classroom.class_name,
      'class_code': classroom.class_code,
      'attendance_pct': class_pct,
      'present': class_present,
      'total': class_total,
    })

  context = {
    'student_profiles': student_profiles,
    'classes': classes,
    'today_schedule': classes,
    'total_classes': len(classes),
    'attendance_pct': attendance_pct,
    'total_attendance': total_attendance,
    'present_attendance': present_attendance,
  }
  return render(request,'student_dashboard.html', context)
