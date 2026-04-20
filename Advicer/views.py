from django.shortcuts import render,redirect
from utils.Codegen import Code
from .models import advicer,Classroom
from django.http import HttpResponse
from HOD.models import Department
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def generate_code(request):
  code_gen=Code()
  if request.method=='POST':
    code=request.POST.get('')

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


def advisor_dashboard(request):
  classroom = Classroom.objects.filter(advisor=request.user).last()
  return render(request,'advisor_dashboard.html',{'classroom':classroom})

def students(request):
  return render(request,'students.html')


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