from collections import defaultdict
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render,redirect
from django.utils import timezone
from django.utils.dateparse import parse_date
from Attendence.models import Attendence
from Class.models import Classes
from Student.models import Student
from .models import Faculty
from django.http import HttpResponse
from Advicer.models import Classroom
# Create your views here.
def faculty_info(request):
  error = None
  if request.method=="POST":
    faculty_id=request.POST.get('faculty_id')
    mobile_num=request.POST.get('mobile_num')
    class_code=request.POST.get('class_code')
    subject_name=request.POST.get('subject_name')
    subject_code=request.POST.get('subject_code')
    
    code = Classroom.objects.filter(class_code=class_code).first()

    if Faculty.objects.filter(faculty_id=faculty_id).exists():
        error = "This advisor ID already exists"
    elif code:
            faculty = Faculty.objects.create(
               username=request.user,
              faculty_id=faculty_id,
              mobile_num=mobile_num,
              class_code=class_code,
              subject_name=subject_name,
              subject_code=subject_code
              )
            Classes.objects.create(class_code=code, subject_code=faculty)
            return redirect("advisor_dashboard")
    else:
            error = "Your code is not Valid"
    return redirect("faculty_dashboard")  

  return render(request,'faculty_info.html')

@login_required
def faculty_dashboard(request):
    faculties = Faculty.objects.filter(username=request.user)

    class_links = Classes.objects.filter(
        subject_code__in=faculties
    ).select_related('class_code', 'subject_code')

    today = timezone.localdate()
    subject_rows = []

    total_students = total_present = total_attendance = 0
    total_classes_done = today_total = today_present = 0

    for link in class_links:
        subject = link.subject_code
        classroom = link.class_code

        students = Student.objects.filter(class_code=classroom.class_code)
        attendance = Attendence.objects.filter(
            subject_code=subject,
            class_code=classroom
        )

        students_count = students.count()
        attendance_total = attendance.count()
        present_count = attendance.filter(is_present=True).count()
        classes_done = attendance.values('date').distinct().count()

        attendance_pct = round(
            (present_count / attendance_total) * 100
        ) if attendance_total else 0

        today_att = attendance.filter(date=today)
        today_count = today_att.count()
        today_pres = today_att.filter(is_present=True).count()

        subject_rows.append({
            'id': link.id,
            'subject_name': subject.subject_name,
            'subject_code': subject.subject_code,
            'class_name': classroom.class_name,
            'class_code': classroom.class_code,
            'students_count': students_count,
            'attendance_pct': attendance_pct,
            'classes_done': classes_done,
        })

        total_students += students_count
        total_present += present_count
        total_attendance += attendance_total
        total_classes_done += classes_done
        today_total += today_count
        today_present += today_pres

    overall_attendance_pct = round(
        (total_present / total_attendance) * 100
    ) if total_attendance else 0

    context = {
        'classes': subject_rows,
        'total_classes': len(subject_rows),
        'total_students': total_students,
        'total_classes_done': total_classes_done,
        'overall_attendance_pct': overall_attendance_pct,
        'today_total': today_total,
        'today_present': today_present,
        'total_pages': 1,
    }

    return render(request, 'faculty_dashboard.html', context)





@login_required
def add_attendence(request, class_link_id=None):
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
        return render(request, 'daily_attendance.html', {
            'class': None,
            'students': [],
            'total_students': 0,
        })

    subject = class_link.subject_code
    classroom = class_link.class_code
    selected_date = parse_date(
        request.POST.get('attendance_date') or request.GET.get('date') or ''
    ) or today

    students = Student.objects.filter(
        class_code=classroom.class_code
    ).select_related('username').order_by('usn')

    if request.method == 'POST':
        for student in students:
            status = request.POST.get(f'attendance_{student.id}')

            if status not in ['present', 'absent']:
                continue

            Attendence.objects.create(
                usn=student,
                subject_code=subject,
                class_code=classroom,
                date=selected_date,
                is_present=(status == 'present'),
            )

        return redirect('add_attendence', class_link_id=class_link.id)

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

    return render(request, 'daily_attendance.html', context)


@login_required
def student_attendence(request):
    faculties = Faculty.objects.filter(username=request.user)
    class_links = Classes.objects.filter(
        subject_code__in=faculties
    ).select_related('class_code', 'subject_code')

    subjects = []
    classrooms = []
    for link in class_links:
        if link.subject_code:
            subjects.append(link.subject_code)
        if link.class_code:
            classrooms.append(link.class_code)

    attendance_records = Attendence.objects.filter(
        subject_code__in=subjects,
        class_code__in=classrooms
    ).select_related('usn', 'usn__username', 'class_code', 'subject_code').order_by('-date', 'usn__usn')

    context = {
        'attendance_records': attendance_records,
        'classes': class_links,
    }
    return render(request, 'faculty_attendance_record.html', context)


@login_required
def student_list(request, class_link_id=None):
    faculties = Faculty.objects.filter(username=request.user)
    class_links = Classes.objects.filter(
        subject_code__in=faculties
    ).select_related('class_code', 'subject_code')

    if class_link_id:
        class_link = get_object_or_404(class_links, id=class_link_id)
    else:
        class_link = class_links.first()

    if not class_link:
        return render(request, 'faculty_student_list.html', {
            'class': None,
            'dates': [],
            'date_columns': [],
            'students': [],
            'total_students': 0,
        })

    subject = class_link.subject_code
    classroom = class_link.class_code

    students = Student.objects.filter(
        class_code=classroom.class_code
    ).select_related('username').order_by('usn')

    if not students.exists():
        students = Student.objects.filter(
            class_code__iexact=str(classroom.class_code).strip()
        ).select_related('username').order_by('usn')

    attendances = Attendence.objects.filter(
        subject_code=subject,
        class_code=classroom,
        usn__in=students
    ).select_related('usn').order_by('date', 'id')

    student_date_records = defaultdict(list)
    max_sessions_by_date = defaultdict(int)
    for attendance in attendances:
        key = (attendance.usn_id, attendance.date)
        student_date_records[key].append(attendance)
        current_count = len(student_date_records[key])
        if current_count > max_sessions_by_date[attendance.date]:
            max_sessions_by_date[attendance.date] = current_count

    dates = []
    date_columns = []
    for date in sorted(max_sessions_by_date.keys()):
        for session in range(1, max_sessions_by_date[date] + 1):
            dates.append(date)
            date_columns.append({
                'date': date,
                'session': session,
            })

    student_rows = []
    for student in students:
        records = []
        present_count = 0
        marked_count = 0
        date_index_tracker = defaultdict(int)
        for date in dates:
            session_index = date_index_tracker[date]
            date_index_tracker[date] += 1
            entries = student_date_records.get((student.id, date), [])
            if session_index >= len(entries):
                status = 'na'
            else:
                status = 'present' if entries[session_index].is_present else 'absent'
            records.append({
                'date': date,
                'status': status,
            })
            if status in ['present', 'absent']:
                marked_count += 1
                if status == 'present':
                    present_count += 1

        percentage = round((present_count / marked_count) * 100) if marked_count else 0

        student_rows.append({
            'first_name': student.username.first_name if student.username else '',
            'last_name': student.username.last_name if student.username else '',
            'student_id': student.usn,
            'records': records,
            'percentage': percentage,
        })

    context = {
        'class': {
            'id': class_link.id,
            'name': subject.subject_name,
            'code': subject.subject_code,
            'class_name': classroom.class_name,
            'class_code': classroom.class_code,
        },
        'dates': dates,
        'date_columns': date_columns,
        'students': student_rows,
        'total_students': len(student_rows),
    }

    return render(request, 'faculty_student_list.html', context)


@login_required
def add_class_as_faculty(request):
  if request.method == 'POST':
    class_code = request.POST.get('class_code')
    subject_name = request.POST.get('subject_name')
    subject_code = request.POST.get('subject_code')

    faculty_profile = Faculty.objects.filter(username=request.user).first()
    if not faculty_profile:
      return HttpResponse("Faculty profile not found. Please complete faculty info first.")

    class_code_str = str(class_code).strip()
    if not class_code_str:
      return HttpResponse("Class code is required.")

    try:
      class_code_int = int(class_code_str)
    except (TypeError, ValueError):
      return HttpResponse("Invalid class code. It must be a number.")

    classroom = Classroom.objects.filter(class_code=class_code_str).first()
    if not classroom:
      return HttpResponse("Classroom not found for the provided class code.")

    faculty_key = f"{faculty_profile.faculty_id}_{subject_code}"
    faculty_obj, _ = Faculty.objects.update_or_create(
      faculty_id=faculty_key,
      defaults={
        'hod': faculty_profile.hod,
        'username': request.user,
        'mobile_num': faculty_profile.mobile_num,
        'class_code': class_code_int,
        'subject_name': subject_name,
        'subject_code': subject_code,
      }
    )

    Classes.objects.update_or_create(
      class_code=classroom,
      subject_code=faculty_obj,
    )

    return redirect('faculty_dashboard')

  return render(request,'add_class_as_faculty.html')

@login_required
def add_marks(request, class_link_id=None):
    faculties = Faculty.objects.filter(username=request.user)
    class_links = Classes.objects.filter(
        subject_code__in=faculties
    ).select_related('class_code', 'subject_code')

    if class_link_id:
        class_link = get_object_or_404(class_links, id=class_link_id)
    else:
        class_link = class_links.first()

    if not class_link:
        return render(request, 'marks_entry.html', {'class': None, 'students': []})

    subject = class_link.subject_code
    classroom = class_link.class_code

    students = Student.objects.filter(
        class_code=classroom.class_code
    ).select_related('username').order_by('usn')

    from marks.models import Marks
    
    if request.method == 'POST':
        for student in students:
            i1 = request.POST.get(f'internal1_{student.id}', 0)
            i2 = request.POST.get(f'internal2_{student.id}', 0)
            
            try:
                i1_val = float(i1) if i1 else 0
                i2_val = float(i2) if i2 else 0
            except ValueError:
                i1_val = 0
                i2_val = 0
            
            Marks.objects.update_or_create(
                student=student,
                subject=subject,
                class_code=classroom,
                defaults={
                    'internal1': i1_val,
                    'internal2': i2_val,
                    'total_marks': i1_val + i2_val
                }
            )
        return redirect('add_marks', class_link_id=class_link.id)

    marks_data = {
        m.student_id: m for m in Marks.objects.filter(subject=subject, class_code=classroom)
    }

    student_rows = []
    for student in students:
        m = marks_data.get(student.id)
        student_rows.append({
            'id': student.id,
            'usn': student.usn,
            'name': student.username.get_full_name() if student.username else student.usn,
            'internal1': m.internal1 if m else 0,
            'internal2': m.internal2 if m else 0,
            'total': m.total_marks if m else 0,
        })

    context = {
        'class_link': class_link,
        'class_links': class_links,
        'students': student_rows,
        'selected_class': class_link,
    }
    return render(request, 'marks_entry.html', context)

  
