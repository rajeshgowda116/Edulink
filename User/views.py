from django.shortcuts import render
from django.http import HttpResponse
from .forms import ResgistrationForm
# Create your views here.
def register(request):
  if request.method=="POST":
    form=ResgistrationForm(request.POST)
    if form.is_valid():
      form.save()
      return HttpResponse("HI BVC ITS dashbord")
  
  else:
    form=ResgistrationForm()
  
  return render(request,'registration.html',{'form':form})
    
