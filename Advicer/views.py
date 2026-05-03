from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse
from marks.models import Marks
from utils.Codegen import Code
from .models import advicer,Classroom
from django.http import HttpResponse
from HOD.models import Department, Hod
from django.contrib.auth.decorators import login_required
from Attendence.models import Attendence
from Student.models import Student
from Faculty.models import Faculty
from Class.models import Classes
import json
from django.utils import timezone
from django.utils.dateparse import parse_date
from collections import defaultdict
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
    advisor_classrooms = Classroom.objects.filter(advisor=request.user).order_by('class_name')
    classroom = None

    class_id = request.GET.get('class_id')
    if class_id:
        classroom = advisor_classrooms.filter(id=class_id).first()
    if not classroom:
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
        'classrooms': advisor_classrooms,
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

@login_required
def advicer_class(request):
    advisor_subjects = Faculty.objects.filter(username=request.user).order_by('subject_name', 'subject_code')

    selected_classroom = None
    selected_class_id = request.GET.get('class_id')
    if selected_class_id:
        selected_classroom = Classroom.objects.filter(
            advisor=request.user,
            id=selected_class_id
        ).first()

    class_rows = []
    for subject in advisor_subjects:
        class_code_str = str(subject.class_code).strip()
        classroom = Classroom.objects.filter(
            advisor=request.user,
            class_code__iexact=class_code_str
        ).first()

        student_count = Student.objects.filter(
            class_code__iexact=class_code_str
        ).count()

        class_rows.append({
            'class_link_id': classroom.id if classroom else '',
            'subject_name': subject.subject_name or 'N/A',
            'subject_code': subject.subject_code or 'N/A',
            'days': '-',
            'student_count': student_count,
            'class_name': classroom.class_name if classroom else '',
            'class_code': class_code_str,
        })

        if not selected_classroom and classroom:
            selected_classroom = classroom

    selected_students = Student.objects.none()
    if selected_classroom:
        selected_students = Student.objects.filter(
            class_code__iexact=str(selected_classroom.class_code).strip()
        ).select_related('username').order_by('usn')

    context = {
        'hod': class_rows,
        'classes': class_rows,
        'total_classes': len(class_rows),
        'selected_classroom': selected_classroom,
        'selected_students': selected_students,
    }
    return render(request, 'advicer_classes.html', context)

@login_required
def advicer_class_add(request):
    if request.method == 'POST':
        class_code = request.POST.get('class_code')
        subject_name = request.POST.get('subject_name')
        subject_code = request.POST.get('subject_code')

        advisor_profile = advicer.objects.filter(username=request.user).first()
        if not advisor_profile:
            return HttpResponse("Advisor profile not found. Please complete advisor info first.")

        class_code_str = str(class_code).strip()
        if not class_code_str:
            return HttpResponse("Class code is required.")
        try:
            class_code_int = int(class_code_str)
        except (TypeError, ValueError):
            return HttpResponse("Invalid class code. It must be a number.")

        linked_hod = None
        dept = Department.objects.filter(dept_code=str(advisor_profile.hod_code)).first()
        if dept:
            linked_hod = Hod.objects.filter(username=dept.username).first()

        faculty_key = f"{advisor_profile.advicer_id}_{subject_code}"
        faculty_obj, _ = Faculty.objects.update_or_create(
            faculty_id=faculty_key,
            defaults={
                'hod': linked_hod,
                'username': request.user,
                'mobile_num': advisor_profile.mobile_num,
                'class_code': class_code_int,
                'subject_name': subject_name,
                'subject_code': subject_code,
            }
        )

        classroom = Classroom.objects.filter(class_code=class_code_str).first()
        if classroom:
            Classes.objects.update_or_create(
                class_code=classroom,
                subject_code=faculty_obj,
            )

        return redirect('advicer_class')

    return render(request, 'advicer_class_add.html')


@login_required
def advicer_add_attendence(request, class_link_id=None):
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
        return render(request, 'advicer_add_attendence.html', {
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

            Attendence.objects.create(
                usn=student,
                subject_code=subject,
                class_code=classroom,
                date=selected_date,
                is_present=(status == 'present'),
            )

        return redirect('advicer_add_attendence', class_link_id=class_link.id)

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
    return render(request, 'advicer_add_attendence.html', context)


@login_required
def advicer_student_attendence_list(request, class_link_id=None):
    faculties = Faculty.objects.filter(username=request.user)
    class_links = Classes.objects.filter(
        subject_code__in=faculties
    ).select_related('class_code', 'subject_code')

    if class_link_id:
        class_link = get_object_or_404(class_links, id=class_link_id)
    else:
        class_link = class_links.first()

    if not class_link:
        return render(request, 'advicer_Student_attendence_list.html', {
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
        count = len(student_date_records[key])
        if count > max_sessions_by_date[attendance.date]:
            max_sessions_by_date[attendance.date] = count

    dates = []
    date_columns = []
    for date in sorted(max_sessions_by_date.keys()):
        for session in range(1, max_sessions_by_date[date] + 1):
            dates.append(date)
            date_columns.append({'date': date, 'session': session})

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
            records.append({'date': date, 'status': status})
            if status in ['present', 'absent']:
                marked_count += 1
                if status == 'present':
                    present_count += 1

        percentage = round((present_count / marked_count) * 100) if marked_count else 0

        student_rows.append({
            'first_name': student.username.first_name if student.username else '',
            'last_name': student.username.last_name if student.username else '',
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
    return render(request, 'advicer_Student_attendence_list.html', context)

def add_marks_asadvisor(request, class_link_id=None):
    faculties = Faculty.objects.filter(username=request.user)
    class_links = Classes.objects.filter(
        subject_code__in=faculties
    ).select_related('class_code', 'subject_code')

    if class_link_id:
        class_link = get_object_or_404(class_links, id=class_link_id)
    else:
        class_link = class_links.first()

    if not class_link:
        return render(request, 'marks.html', {
            'classes': class_links,
            'students': [],
            'selected_class_link': None
        })

    subject = class_link.subject_code
    classroom = class_link.class_code

    # Fetch students for this classroom (more robust filtering)
    students = Student.objects.filter(
        class_code=classroom.class_code
    ).select_related('username').order_by('usn')

    if not students.exists():
        students = Student.objects.filter(
            class_code__iexact=str(classroom.class_code).strip()
        ).select_related('username').order_by('usn')

    if request.method == 'POST':
        # Use student IDs or USNs to get marks from POST data
        all_students = Student.objects.filter(
            class_code__iexact=str(classroom.class_code).strip()
        ) | Student.objects.filter(class_code=classroom.class_code)
        
        for student in all_students.distinct():
            int1_val = request.POST.get(f'int1_{student.id}')
            int2_val = request.POST.get(f'int2_{student.id}')

            if int1_val is None and int2_val is None:
                continue

            try:
                int1 = float(int1_val) if (int1_val is not None and int1_val.strip() != '') else 0
                int2 = float(int2_val) if (int2_val is not None and int2_val.strip() != '') else 0
            except ValueError:
                int1 = 0
                int2 = 0

            Marks.objects.update_or_create(
                student=student,
                class_code=classroom,
                subject=subject,
                defaults={
                    'internal1': int1,
                    'internal2': int2,
                    'total_marks': int1 + int2
                }
            )
        return redirect(reverse('add_marks_asadvisor', kwargs={'class_link_id': class_link.id}) + '?success=true')

    # Fetch existing marks records
    marks_records = Marks.objects.filter(
        subject=subject,
        class_code=classroom,
        student__in=students
    )
    marks_dict = {m.student_id: m for m in marks_records}

    student_data = []
    for student in students:
        m = marks_dict.get(student.id)
        # Only show as empty string if no record exists, otherwise show the mark
        student_data.append({
            'id': student.id,
            'usn': student.usn,
            'first_name': student.username.first_name if student.username else '',
            'last_name': student.username.last_name if student.username else '',
            'int1': m.internal1 if m else '',
            'int2': m.internal2 if m else '',
            'total': m.total_marks if m else 0
        })

    context = {
        'classes': class_links,
        'selected_class_link': class_link,
        'students': student_data,
        'total_students': len(student_data),
        'max_internal1': 50,
        'max_internal2': 50,
        'max_total': 100,
        'saved_success': request.GET.get('success') == 'true',
    }
    return render(request, 'add-marks.html', context)

def show_marks(request, class_link_id=None):
    faculties = Faculty.objects.filter(username=request.user)
    class_links = Classes.objects.filter(
        subject_code__in=faculties
    ).select_related('class_code', 'subject_code')

    if class_link_id:
        class_link = get_object_or_404(class_links, id=class_link_id)
    else:
        class_link = class_links.first()

    if not class_link:
        return render(request, 'marks-show.html', {
            'classes': class_links,
            'students': [],
            'selected_class_link': None
        })

    subject = class_link.subject_code
    classroom = class_link.class_code

    # Fetch students for this classroom
    students = Student.objects.filter(
        class_code=classroom.class_code
    ).select_related('username').order_by('usn')

    if not students.exists():
        students = Student.objects.filter(
            class_code__iexact=str(classroom.class_code).strip()
        ).select_related('username').order_by('usn')

    # Fetch existing marks records
    marks_records = Marks.objects.filter(
        subject=subject,
        class_code=classroom,
        student__in=students
    )
    marks_dict = {m.student_id: m for m in marks_records}

    student_data = []
    total_marks_sum = 0
    highest_mark = 0
    lowest_mark = 100 if marks_records.exists() else 0
    highest_student = "N/A"
    lowest_student = "N/A"

    for student in students:
        m = marks_dict.get(student.id)
        current_total = m.total_marks if m else 0
        
        # Stats logic
        if m:
            total_marks_sum += current_total
            if current_total >= highest_mark:
                highest_mark = current_total
                highest_student = f"{student.username.first_name} {student.username.last_name}" if student.username else student.usn
            if current_total <= lowest_mark:
                lowest_mark = current_total
                lowest_student = f"{student.username.first_name} {student.username.last_name}" if student.username else student.usn

        student_data.append({
            'name': f"{student.username.first_name} {student.username.last_name}" if student.username else "N/A",
            'usn': student.usn,
            'internal1': m.internal1 if m else 0,
            'internal2': m.internal2 if m else 0,
            'total': current_total
        })

    avg_marks = round(total_marks_sum / len(marks_records), 2) if marks_records.exists() else 0

    context = {
        'classes': class_links,
        'selected_class_link': class_link,
        'students': student_data,
        'total_students': len(student_data),
        'avg_marks': avg_marks,
        'highest_mark': highest_mark,
        'highest_student': highest_student,
        'lowest_mark': lowest_mark,
        'lowest_student': lowest_student,
        'max_total': 100,
    }

    return render(request, 'show_marks.html', context)
