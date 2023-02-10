import re
from django.shortcuts import render, redirect
from .forms import CustomUserCreateForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .forms import MatchRegisterForm
from .models import Team, MatchInfo, Stadium, Alarm
import datetime
# Create your views here.





def match_detail(request, pk): # pk = 매치 아이디

  user = request.user
  match = MatchInfo.objects.get(id=pk)
  match = get_object_or_404(MatchInfo, pk = pk)
  
  if match.host_id == request.user:
    context={
      "user" : user, 
      "match" : match,
      "status": 1
    }
    
  else: 
    context={
      "user" : user, 
      "match" : match,
      "status": 0
    }

  return render(request, "matchingMatch/match_detail.html", context=context)



def team_detail(request, pk): # pk = 팀 아이디

  user = request.user

  match = get_object_or_404(Team, pk = pk)

  context = {"user" : user, "match" : match}

  return render(request, "html", context=context)



@login_required
def team_update(request, pk):
  match = get_object_or_404(Team, pk = pk)
  if request.method == "POST":
    match_form = CustomUserCreateForm(request.POST)
    if match_form.is_valid():
      match_form.save()
      return redirect("/")
    else:
      return render()
  else:
    match_form = CustomUserCreateForm(instance=match)
    context = {"match_form" : match_form}

    return render(request, "html", context=context)



def my_page(request, pk): # pk = 유저 아이디
  #아직 어떤 기능을 넣을지 미정
  pass



def match_register(request):
  
  if request.method == "POST":
    match_form = MatchRegisterForm(request.POST)
    

    
    if match_form.is_valid():
      match = match_form.save(commit=False)
      match.host_id = request.user
      match.save()
      return redirect("/")
    else:
      print(match_form.cleaned_data)
      stadium_name = Stadium.objects.all()
      stadium_name_list = stadium_name
      context = {"match_form" : match_form ,"stadium_name":stadium_name,"stadium_name_list":stadium_name_list,}
      return render(request, "matchingMatch/match_register.html", context=context)
    
  else:
    stadium_name = Stadium.objects.all()
    stadium_name_list = stadium_name
    match_form = MatchRegisterForm()
    context = {"match_form" : match_form , "stadium_name":stadium_name, "stadium_name_list":stadium_name_list,}
  
    return render(request, "matchingMatch/match_register.html", context=context)


# def match_select(request, pk): 매치 선택

# def match_cancel(request, pk): 매치 취소
# 1. 이미 성사된 매치의 경우
# 2. 그냥 신청만 한 경우

# def match_open(request, pk):

def match_update(request, pk):
  
  if request.method == "POST":
    match_form = MatchRegisterForm(request.POST)
    if match_form.is_valid():
      id = match_form.save()
      return redirect("/") # 수정된 페이지로 이동
    
    else:
      return redirect("/") # 다시 작성하기
  
  else:
    match_form = MatchRegisterForm()
    context = {"match_form" : match_form}
    return render(request, "html", context=context)


#매치 결정
def match_resolve(request, pk): # pk = 매치 아이디
  
  if request.method == "POST":
    match = get_object_or_404(MatchInfo, id = pk)
    match.participant_id = request.user.pk
    match.is_matched = True
    match.save()
    return redirect("/")

  return render(request, "html")


def main(request, *args, **kwargs):
    
    alarm = Alarm.objects.filter(team_id=request.user.pk)
    return render(request, "matchingMatch/main.html", {'alarm': alarm})


def endOfGame(request, *args, **kwargs):
    return render(request, "matchingMatch/endOfGame.html")


def check_endOfGame():
    # 날짜 셋팅
    now = datetime.datetime.now()

    MatchInfos = MatchInfo.objects.filter(
        is_alarmed=False)  # 알람이 생성되지 않은 매치: 경기가 끝나지 않은 매치들

    if len(MatchInfos) != 0:
        for match in MatchInfos:
            matchTime = match.end_time.replace(tzinfo=None)
            if matchTime < now:
                match.is_alarmed = True
                match.save()
                Alarm.objects.create(
                    team_id=match.host_id,
                    match_id=match
                )

                Alarm.objects.create(
                    team_id=match.participant_id,
                    match_id=match
                )

def login_page(request):
    page = 'matchingMatch:login'

    if request.method == "POST":
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
            )

        if user is not None:
            login(request, user)
            messages.info(request, '성공적으로 로그인 하셨습니다.')
            return redirect('matchingMatch:home') 
        else:
            messages.error(request, '이메일 혹은 비밀번호를 다시 확인해주세요.')
            return redirect('matchingMatch:login')
    
    context = {'page':page}
    return render(request, 'matchingMatch/login_register.html', context)

def register_page(request):
    form = CustomUserCreateForm()

    if request.method == 'POST':
        form = CustomUserCreateForm(request.POST, request.FILES,)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            messages.success(request, '성공적으로 회원가입이 진행됐습니다.')
            return redirect('matchingMatch:home')
        else:
            messages.error(request, '회원가입 도중에 문제가 발생하였습니다.')


    page = 'register'
    context = {'page':page, 'form':form}
    return render(request, 'matchingMatch/login_register.html', context)

def logout_user(request):
    logout(request)
    messages.info(request, '로그아웃 상태입니다.')
    return redirect('matchingMatch/login')

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