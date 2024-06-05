from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Profile

# Create your views here.


def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if email == "" or password == "":
            messages.warning(request, "Please fill all Mandatory Fields.")
            return HttpResponseRedirect(request.path_info)

        user_obj = User.objects.filter(username=email)
        if not user_obj.exists():
            messages.warning(request, "Please Check Email Address.")
            return HttpResponseRedirect(request.path_info)

        login_user = authenticate(username=email, password=password)
        if login_user:
            login(request, login_user)
            login_flag = request.session.get('login_flag', False)
            if 'login_flag' in request.session:
                del request.session['login_flag']
            if False == login_flag:
                return HttpResponseRedirect("/home/login")
            else:
                return HttpResponseRedirect(login_flag)
        else:
            messages.warning(request, "Please Check Password Once.")
            return HttpResponseRedirect(request.path_info)
    return render(request, 'login.html')


def user_register(request):
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "register":
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            email = request.POST.get("email")
            password = request.POST.get("password")
            registeras = request.POST.get("registeras")

            if first_name == "" or last_name == "" or email == "" or password == "":
                messages.warning(request, "Please fill all Mandatory Fields.")
                return HttpResponseRedirect(request.path_info)

            user_obj = User.objects.filter(username=email)
            if user_obj.exists():
                messages.warning(request, "This Email is already used.")
                return HttpResponseRedirect(request.path_info)

            new_user = User.objects.create(
                first_name=first_name, last_name=last_name, username=email
            )
            new_user.set_password(password)
            new_user.save()

            Profile.objects.create(user=new_user, registeras=registeras)

            return HttpResponseRedirect('/user')
    return render(request, 'register.html')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/user')
