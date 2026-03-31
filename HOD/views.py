from django.shortcuts import render

# Create your views here.
def hod_dashboard(request):
  return render(request,'hod_dashboard.html')