from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
# Create your views here.
from .models import User as new_user , Account

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
            login_users = new_user.objects.all()
            acc_details = Account.objects.all()
            data={
                'login_users':login_users,
                'acc_details':acc_details
            }
            return render(request, 'home.html', {'data':data})
        else:
            messages.info(request, 'Invalid credentials')
    return redirect('/')
        

def logout(request):
    auth.logout(request)
    return redirect('/')
        
def create_account(request):
    account_type = request.POST['account_type']
    if Account.objects.exists():
        last_account = Account.objects.latest('account_number')
        account_number = int(last_account.account_number) + 1
    else:
        account_number = 1000001

    user_id = request.POST['user_id']
    login_user = new_user.objects.filter(user_id=user_id).first()
    login_user.has_account = True
    login_user.save()

    new_account = Account(
        account_type=account_type,
        balance=0,
        account_number=str(account_number),
        user_id=user_id
    )
    new_account.save()
    login_users = new_user.objects.all()
    acc_details = Account.objects.all()
    data={
        'login_users':login_users,
        'acc_details':acc_details
    }
    return render(request, 'home.html', {"data" : data})

