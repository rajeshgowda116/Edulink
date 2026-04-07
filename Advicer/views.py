from django.shortcuts import render,redirect
from utils.Codegen import Code
from .models import advicer
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def generate_code(request):
  code_gen=Code()
  if request.method=='POST':
    code=request.POST.get('')

@login_required
def advicer_info(request):
  if request.method=='POST':
    advicer_id=request.POST.get('advicer_id')
    mobile_num=request.POST.get('mobile_num')
    hod_code=request.POST.get('hod_code')
    advicer.objects.create(
        username=request.user,
        advicer_id=advicer_id,
        mobile_num=mobile_num,
        hod_code=hod_code
        )
    return redirect("advisor_dashboard")  
  return render(request,'advisor_form.html')

def advisor_dashboard(request):
  return render(request,'advisor_dashboard.html')