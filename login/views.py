from django.shortcuts import render, redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
# Create your views here.
from .models import User as new_user

def loginpage(request):
    return render(request, 'login.html', {})

def register(request):
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    password = request.POST['password']
    email = request.POST['email']
    username = request.POST['username']
    phone_number = request.POST['phone_number']
    address = request.POST['address']
    confirm_password = request.POST['confirm_password']
    date_of_birth = request.POST['date_of_birth']

    if password == confirm_password:
        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username taken')   
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Email taken')
        else:
            user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
            user.save()
            messages.info(request, 'User created')
            messages.info(request, 'Please login')
            # add to the login_users table
            login_user = new_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date_of_birth,
                address=address,
                phone_number=phone_number
            )
            login_user.save()
    else:
        messages.info(request, 'Password not matching')
    return redirect('/')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return render(request, 'home.html', {})
        else:
            messages.info(request, 'Invalid credentials')
    return redirect('/')
        

def logout(request):
    auth.logout(request)
    return redirect('/')
        
