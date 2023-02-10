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
  # Review : 권한 제한 없이 누구나 볼 수 있는 건가요?

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

  team = get_object_or_404(Team, pk = pk)

  context = {"user" : user, "team" : team}

  return render(request, "html", context=context)



@login_required(login_url='/login')
def team_update(request, pk):

  team = get_object_or_404(Team, pk = pk)
  if not (request.user == team.host_id or request.user == team.participant_id):
    # return redirect("matchingMatch:team_detail", pk = team.pk)
    return redirect("/")

  if request.method == "POST":
    team_form = CustomUserCreateForm(request.POST, instance=pk)
    if team_form.is_valid():
      team_form.save()
      return redirect("/")
    else:
      return render()
  else:
    team_form = CustomUserCreateForm(instance=pk)
    context = {"team_form" : team_form}

    return render(request, "html", context=context)





def my_page(request, pk): # pk = 유저 아이디
  #아직 어떤 기능을 넣을지 미정
  pass


@login_required(login_url='/login')
def match_register(request):
  
  if request.method == "POST":
    match_form = MatchRegisterForm(request.POST)
    
    if match_form.is_valid():
      match = match_form.save(commit=False)
      match.host_id = request.user
      match.save()
      return redirect("/")
    else:
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

@login_required(login_url='/login')
def match_select(request, pk): # 매치 신청 ajax로 해보는 게 좋을듯

  if request.method == "POST":
    match = get_object_or_404(MatchInfo, id = pk)
    #신청한 리스트에 현재 본인의 것이 존재하는지 여부를 확인
    if match.is_matched:
      
      messages.error(request, '이미 상대가 결정된 경기입니다.')
      return redirect("/")
    else:
      messages.success(request, '경기 신청이 완료되었습니다.')
      return redirect("/")

@login_required(login_url='/login')
def match_cancel(request, pk): #매치 신청 취소
  match = get_object_or_404(MatchInfo, id=pk)

  if match.is_matched == False:
    # 매치 신청목록에서 이미 자신의 것이 있는 경우 돌아가기
    # 있을 경우 신청 취소
    return
  else:
    #이미 매치가 성사된 경우는 일단 보류
    ...
  

# def match_open(request, pk):

@login_required(login_url='/login')
def match_update(request, pk):
  
  if request.method == "POST":
    match_form = MatchRegisterForm(request.POST, instance=pk)
    if match_form.is_valid():
      match = match_form.save()
      return redirect("/") # 수정된 페이지로 이동
    
    else:
      return redirect("/") # 다시 작성하기
  
  else:
    match_form = MatchRegisterForm(instance=pk)
    context = {"match_form" : match_form}
    return render(request, "html", context=context)


#매치 결정
@login_required(login_url='/login')
def match_resolve(request, pk): # pk = 매치 아이디
  
  if request.method == "POST":
    match = get_object_or_404(MatchInfo, id = pk)
    match.participant_id = request.user
    match.is_matched = True
    match.save()
    return redirect("matchingMatch:match_detail", pk = match.pk)

  return render(request, "html")


def main(request, *args, **kwargs):
    
    alarm = Alarm.objects.filter(team_id=request.user.pk)
    return render(request, "matchingMatch/main.html", {'alarm': alarm})


def endOfGame(request, *args, **kwargs):
    return render(request, "matchingMatch/endOfGame.html")


# def check_endOfGame():
#     # 날짜 셋팅
#     # Review : 알람 기능인 것 같은데, 알람 기능은 조금 복잡합니다.
#     # Review : 참고해보세요! https://dongsik93.github.io/til/2019/07/31/til-etc-fcm/
#     now = datetime.datetime.now()

#     MatchInfos = MatchInfo.objects.filter(
#         is_alarmed=False)  # 알람이 생성되지 않은 매치: 경기가 끝나지 않은 매치들

#     if len(MatchInfos) != 0:
#         for match in MatchInfos:
#             matchTime = match.end_time.replace(tzinfo=None)
#             if matchTime < now:
#                 match.is_alarmed = True
#                 match.save()
#                 Alarm.objects.create(
#                     team_id=match.host_id,
#                     match_id=match
#                 )

#                 Alarm.objects.create(
#                     team_id=match.participant_id,
#                     match_id=match
#                 )

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
    return redirect('login')

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