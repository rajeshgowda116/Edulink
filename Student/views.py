from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from Advicer.models import Classroom
from Attendence.models import Attendence
from .models import Student
from Class.models import Classes
from marks.models import Marks

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

@login_required
def Student_dashbord2(request):
    student = Student.objects.filter(username=request.user).first()
    if not student:
        return redirect('student_info')
    
    classroom = Classroom.objects.filter(class_code=student.class_code).first()
    if not classroom:
        context = {
            'student': student,
            'classes': [],
            'total_classes': 0,
            'avg_attendance': 0,
            'avg_internal1': 0,
            'avg_internal2': 0,
        }
        return render(request, 'student_dashboard2.html', context)

    # Get all subjects for this classroom via Classes model
    class_links = Classes.objects.filter(class_code=classroom).select_related('subject_code', 'subject_code__username')
    
    classes_data = []
    total_present = 0
    total_marked = 0
    total_internal1 = 0
    total_internal2 = 0
    marks_count = 0
    
    colors = ['blue', 'green', 'purple', 'orange', 'pink', 'teal']
    
    for i, link in enumerate(class_links):
        subject = link.subject_code
        if not subject:
            continue
            
        # Attendance for this student in this subject
        attendance_records = Attendence.objects.filter(usn=student, subject_code=subject)
        total_count = attendance_records.count()
        present_count = attendance_records.filter(is_present=True).count()
        
        attendance_pct = round((present_count / total_count) * 100) if total_count > 0 else 0
        
        # Marks for this student in this subject
        marks = Marks.objects.filter(student=student, subject=subject).first()
        internal1 = marks.internal1 if marks else 0
        internal2 = marks.internal2 if marks else 0
        
        total_internal1 += internal1
        total_internal2 += internal2
        marks_count += 1
        
        # Calculate stroke-dashoffset: 169.6 is the full circle
        att_offset = 169.6 * (1 - attendance_pct / 100)
        
        # Abbreviation for UI
        abbr = "".join([w[0] for w in subject.subject_name.split() if w])[:2].upper() if subject.subject_name else "SB"
        
        # Define color map for hex values
        color_map = {
            'blue': '#2563eb',
            'green': '#16a34a',
            'purple': '#7c3aed',
            'orange': '#f59e0b',
            'pink': '#ec4899',
            'teal': '#0891b2'
        }
        current_color = colors[i % len(colors)]
        
        classes_data.append({
            'color': current_color,
            'color_hex': color_map.get(current_color, '#2563eb'),
            'abbr': abbr,
            'code': subject.subject_code,
            'name': subject.subject_name,
            'faculty': subject.username.get_full_name() if subject.username else "Faculty",
            'attendance': attendance_pct,
            'att_offset': round(att_offset, 1),
            'internal1': internal1,
            'internal2': internal2,
            'attended': present_count,
            'total': total_count,
            'type': 'Theory'
        })

        
        total_present += present_count
        total_marked += total_count

    avg_attendance = round((total_present / total_marked) * 100) if total_marked > 0 else 0
    avg_internal1 = round((total_internal1 / (marks_count * 50)) * 100) if marks_count > 0 else 0
    avg_internal2 = round((total_internal2 / (marks_count * 50)) * 100) if marks_count > 0 else 0
    
    context = {
        'student': student,
        'classes': classes_data,
        'total_classes': len(classes_data),
        'avg_attendance': avg_attendance,
        'avg_internal1': avg_internal1,
        'avg_internal2': avg_internal2,
    }
    
    return render(request, 'student_dashboard2.html', context)



