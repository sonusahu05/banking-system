from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.loginpage, name='loginpage'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('create_account', views.create_account, name='create_account'),
    path('transfer' , views.transfer, name='transfer'),
    path('deposit' , views.deposit, name='deposit'),
    path('withdraw' , views.withdraw, name='withdraw'),

]
