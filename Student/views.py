from django.shortcuts import render,redirect
from .models import Student
# Create your views here.
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

def student_dashboard(request):
  return render(request,'student_dashboard.html')