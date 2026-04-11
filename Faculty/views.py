from django.shortcuts import render
from .models import Faculty
from django.http import HttpResponse
# Create your views here.
def faculty_info(request):
  if request.method=="POST":
    faculty_id=request.POST.get('faculty_id')
    mobile_num=request.POST.get('mobile_num')
    class_code=request.POST.get('class_code')
    subject_name=request.POST.get('subject_name')
    subject_code=request.POST.get('subject_code')
    Faculty.objects.create(
        username=request.user,
        faculty_id=faculty_id,
        mobile_num=mobile_num,
        class_code=class_code,
        subject_name=subject_name,
        subject_code=subject_code
        )
    return HttpResponse("HIII lowde")  

  return render(request,'faculty_info.html')

def faculty_dashboard(request):
  return render(request, 'faculty_dashboard.html')

def add_attendence(request):
  return render(request,'daily_attendance.html')

def student_attendence(request):
  return render(request,'faculty_attendance_record.html')

  
