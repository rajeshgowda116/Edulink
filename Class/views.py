from django.shortcuts import render
from django.http import HttpResponse
from Class.models import Classes
# Create your views here.
def Calculate(request):
  classes = Classes.objects.all()
  codes = []

  for clas in classes:
    codes.append({
      'class_code': clas.class_code.class_code if clas.class_code else '',
      'subject_code': clas.subject_code.subject_code if clas.subject_code else '',
    })

  return HttpResponse(f"{codes}")


