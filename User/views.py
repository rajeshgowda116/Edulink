from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import ResgistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
# Create your views here.
def register(request):
    if request.method == "POST":
        form = ResgistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # 🔐 hash password
            user.set_password(form.cleaned_data['password1'])
            user.save()

            # 🔥 auto login
            auth.login(request, user)

            role = user.role

            # 🔥 role-based redirect
            if role == 'advisor':
                return redirect('advicer_info')

            elif role == 'hod':
                return redirect('hod_info')

            elif role == 'faculty':
                return redirect('faculty_info')

            elif role == 'student':
                return redirect('student_info')

    else:
        form = ResgistrationForm()

    return render(request, 'registration.html', {'form': form})


def login(requset):
  if requset.method=='POST':
    form=AuthenticationForm(requset,data=requset.POST)
    if form.is_valid():
      user=form.get_user()
      selected_role = requset.POST.get('role')
      if selected_role and user.role != selected_role:
        form.add_error(None, "Selected role does not match your account.")
      else:
        auth.login(requset,user)
        role = user.selected_role
        if role == 'advisor':
           return redirect('advisor_dashboard')
        elif role == 'hod':
            return redirect('hod_dashboard')

        elif role == 'faculty':
            return redirect('faculty_info')

        elif role == 'student':
             return redirect('student_dashboard')
        
  else:
      form=AuthenticationForm()
  return render(requset,'login.html',{'form':form})
    
