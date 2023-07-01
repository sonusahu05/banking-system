from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
# Create your views here.
from .models import User as new_user , Account, Transaction

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
            cur=user.username
            login_users = new_user.objects.filter(username=cur).first()
            if login_users.has_account == False:
                return render(request, 'home.html', {'data' : None})
            else:
                a=login_users.user_id
                acc_details = Account.objects.filter(user_id=a).first()
                return render(request, 'home.html', {'data':acc_details})
        else:
            messages.info(request, 'Invalid credentials')
    return redirect('/')
        

def logout(request):
    auth.logout(request)
    return redirect('/')
        
def create_account(request):
    account_type = request.POST['account_type']
    username = request.user.username
    user = new_user.objects.filter(username=username).first()
    user_id = user.user_id
    user.has_account = True
    user.save()

    new_account = Account(
        account_type=account_type,
        balance=0,
        user_id=user_id
    )
    new_account.save()
    acc_details = Account.objects.filter(user_id=user_id).first()
    return render(request, 'home.html', {'data':acc_details})


def transfer(request):
    acc=request.POST['from_account']
    to_acc=request.POST['to_account']
    amount=request.POST['amount']
    account= Account.objects.filter(account_id=acc).first()
    if account.balance<int(amount):
        messages.info(request, 'Insufficient balance')
    else:
        account.balance=account.balance-int(amount)
        account.save()
        account2= Account.objects.filter(account_id=to_acc).first()
        account2.balance=account2.balance+int(amount)
        account2.save()
        transfer = Transaction(
            account=account,
            receiver_account_number=to_acc,
            amount=amount,
            transaction_type='debit',
            transaction_date=datetime.now()
        )
        transfer.save()
    return render(request, 'home.html', {'data':account})
    

def deposit(request):
    acc=request.POST['acc']
    amount=request.POST['amount']
    account= Account.objects.filter(account_id=acc).first()
    account.balance=account.balance+int(amount)
    account.save()
    transfer = Transaction(
            account=account,
            receiver_account_number=acc,
            amount=amount,
            transaction_type='credit',
            transaction_date=datetime.now()
        )
    transfer.save()
    return render(request, 'home.html', {'data':account})

def withdraw(request):
    acc=request.POST['acc2']
    amount=request.POST['amount']
    account= Account.objects.filter(account_id=acc).first()
    if account.balance<int(amount):
        messages.info(request, 'Insufficient balance')
    else:
        account.balance=account.balance-int(amount)
        account.save()
        transfer = Transaction(
            account=account,
            receiver_account_number=acc,
            amount=amount,
            transaction_type='debit',
            transaction_date=datetime.now()
        )
        transfer.save()
    return render(request, 'home.html', {'data':account})