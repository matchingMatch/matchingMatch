import re
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import CustomUserCreateForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

def login_page(request):
    page = 'login'

    if request.method == "POST":
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
            )

        if user is not None:
            login(request, user)
            messages.info(request, '성공적으로 로그인 하셨습니다.')
            return redirect('home') 
        else:
            messages.error(request, '이메일 혹은 비밀번호를 다시 확인해주세요.')
            return redirect('login')
    
    context = {'page':page}
    return render(request, 'login_register.html', context)

def register_page(request):
    form = CustomUserCreateForm()

    if request.method == 'POST':
        form = CustomUserCreateForm(request.POST, request.FILES,)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            messages.success(request, '성공적으로 회원가입이 진행됐습니다.')
            return redirect('home')
        else:
            messages.error(request, '회원가입 도중에 문제가 발생하였습니다.')


    page = 'register'
    context = {'page':page, 'form':form}
    return render(request, 'login_register.html', context)

def logout_user(request):
    logout(request)
    messages.info(request, '로그아웃 상태입니다.')
    return redirect('login')

def home_page(request):
    return render(request, 'home.html')

@login_required(login_url='/login')
def account_page(request):
    user = request.user

    # img = user.avatar
    # img = Image.open(user.avatar)
    # newsize = (10, 10)
    # img = img.resize(newsize)
  
    # user.avatar = img
    # user.save()
    # user.save()

    context = {'user':user}
    return render(request, 'account.html', context)