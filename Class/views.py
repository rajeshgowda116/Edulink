from django.shortcuts import render
from django.http import HttpResponse
from Class.models import Classes
from Attendence.models import Attendence
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def Calculate(request):
  classes = Classes.objects.all()
  codes = []

  for clas in classes:
    codes.append({
  'class_code': clas.class_code.class_code,
  'class_name': clas.class_code.class_name,
  'subject_code': clas.subject_code.subject_code,
  'subject_name': clas.subject_code.subject_name,
   })
  for code in codes:
    total = Attendence.objects.filter(
    class_code__class_code=code['class_code'],
    subject_code__subject_code=code['subject_code']
    ).count()
    present = Attendence.objects.filter(
    class_code__class_code=code['class_code'],
    subject_code__subject_code=code['subject_code'],
    is_present=True
    ).count()
    
    if total > 0:
      percentage = (present * 100) / total
    else:
      percentage = 0
 
    return HttpResponse(f"<h1>{code['class_name']} {percentage}</h1>")



