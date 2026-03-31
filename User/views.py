from django.shortcuts import render
from django.http import HttpResponse
from .forms import ResgistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
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


def login(requset):
  if requset.method=='POST':
    form=AuthenticationForm(requset,data=requset.POST)
    if form.is_valid():
      user=form.get_user()
      auth.login(requset,user)
      return HttpResponse("hi bvc this is dashbord")
  else:
      form=AuthenticationForm()
  return render(requset,'login.html',{'form':form})
    
