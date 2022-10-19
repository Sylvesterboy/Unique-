from django.shortcuts import redirect, render
from django.contrib import admin
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from Unique import settings
from django.core.mail import send_mail

import testapp

# Create your views here.


def index(request):
    return render(request, "testapp/index.html")

def ok(request):
    return render(request, "testapp/ok.html")    

def signin(request):

    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username = username, password = pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "testapp/index.html", {'fname':fname})
        else:
            messages.error(request, "Bad Credentials!")
            return redirect('index')    

    return render(request, "testapp/signin.html")

def signup(request):

    if request.method == "POST" :
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username = username):
            messages.error(request, "Username already exist! Please try username")
            return redirect('index')

        #if User.object.filter(email = email):
         #   messages.error(request, "Email already registered!")
          #  return redirect('index')

        if len(username)>10:
            messages.error(request, "Username must be underf 10 character")
    

        if pass1 != pass2:
            messages.error(request, "Password didn't match")

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!")
            return redirect('index')    
                           


        myuser = User.objects.create_user(username,fname,lname)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()
        messages.success(request, "Your Account has been successfully created. We have sent you a confirmation email, please confirm your email in order to activate your account.")

        #Welcome Email

        subject = "Welcome to Unique world-Django Login!!"
        message = "Hello" + myuser.first_name + "!! \n" + "Welcome to unique world!! \n Thankyou for visting our website \n We have also sent you a confirmation email, please confirm your email address in order to activate your account. \n\n Thanking you \n unique world"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently = True)


        return redirect('signin')

    return render(request, "testapp/signup.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Sucessfully!")
    return redirect('index')            