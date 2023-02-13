import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .forms import MatchRegisterForm
from .models import Team, MatchInfo, Stadium
from django.db.models import Q
from .models import Team, MatchInfo, Stadium, MatchRequest
from .forms import CustomUserCreateForm, UserForm
from .decorator import admin_required
import re
import datetime
import json

# Create your views here.


def match_detail(request, pk):  # pk = 매치 아이디

  team = request.user
  match = get_object_or_404(MatchInfo, pk = pk)

  try:
    MatchRequest.objects.get(team_id=team)
    context={
      "user" : team, 
      "match" : match,
      "status": 1
    }
  except:
    context={
      "user" : team, 
      "match" : match,
      "status": 0
    }

  return render(request, "matchingMatch/match_detail.html", context=context)


def team_detail(request, pk):  # pk = 팀 아이디
  user = request.user

  team = get_object_or_404(Team, id = pk)
  match_list = MatchInfo.objects.filter(host_id =team)
  context = {"user" : user, "team" : team, "match_list" : match_list}

  return render(request, "matchingMatch/team_detail.html", context=context)


def team_list(request):
  order = request.GET.get("order")
  search = request.GET.get("team_search")
  
  print(order)
  if order:
    teams = Team.objects.order_by(order)
  else:
    teams = Team.objects.all()
  
  if search != None:
    teams = teams.filter(team_name__contains = search)
  #order와 search가 동시에 존재하는 경우?
  context = {"teams" : teams, 
            "order" : order}
  return render (request, "matchingMatch/team_list.html", context=context)


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



@csrf_exempt
def match_cancel(request): #매치 신청 취소
  body_unicode = request.body.decode('utf-8')
  
  req = json.loads(body_unicode) 
  match_request = get_object_or_404(MatchRequest, team_id = req['team.id'])

  match_request.delete()

  status = not req['status']

  return JsonResponse({'status' : status})

  

@csrf_exempt
def match_request(request): #매치 신청
  body_unicode = request.body.decode('utf-8')
  
  req = json.loads(body_unicode)
  
  MatchRequest.objects.create(match_id = req['match.id'], team_id = req['team.id'])
  status = not req['status']

  return JsonResponse({'status' : status})



@login_required(login_url='/login')
def match_update(request, pk):
  match = get_object_or_404(MatchInfo, id=pk)
  if request.method == "POST":
    print(match.id)
    match_form = MatchRegisterForm(request.POST, instance=match)
    if match_form.is_valid():
      match = match_form.save(commit=False)
      match.save()
      return redirect("matchingMatch:match_detail", pk= pk) # 수정된 페이지로 이동
    
    else:
      context = {"match_form" : match_form}
      #잘못된 부분 수정 요청

      return render(request, "matchingMatch/match_update.html", context) # 다시 작성하기
  
  else:
    match_form = MatchRegisterForm(instance=match)
    context = {"match_form" : match_form}
    return render(request, "matchingMatch/match_update.html", context=context)






def match_delete(request, pk): #매치 자체를 없애기 매치를 없애면 어떤 게 생기나?

  if request.method == "POST":
    match = get_object_or_404(MatchInfo, id = pk)
    match.delete()
    return redirect("/")




# team detail과 다른 점?
def my_page(request, pk): # pk = 유저 아이디
  #아직 어떤 기능을 넣을지 미정
  pass





def main(request, *args, **kwargs):
    matches = MatchInfo.objects.filter(is_matched=False)
    userMatches = (MatchInfo.objects.filter(is_alarmed=False) & MatchInfo.objects.filter(
        Q(host_id=request.user.pk) | Q(participant_id=request.user.pk)))
    
    match_detail_category = {
      'gender' : 'gender__in',
      'region' : 'region__in',
      'date' : 'date__in'
    }
    # html 태그 상의 name  : html 태그 상의 value   
    filter_set = {match_detail_category.get(key) : value for key, value in dict(request.GET).items()}
    
    #매치 상세설정
    
    
    # matches = MatchInfo.objects.filter(is_alarmed=False)
    matches = MatchInfo.objects.filter(**filter_set)
    
    context = {
        'matches': matches,
        'userMatches': userMatches,

    }
    return render(request, "matchingMatch/main.html", context=context)

# def check_endOfGame():
#     # 날짜 셋팅
#     # Review : 알람 기능인 것 같은데, 알람 기능은 조금 복잡합니다.
#     # Review : 참고해보세요! https://dongsik93.github.io/til/2019/07/31/til-etc-fcm/
#     now = datetime.datetime.now()

@csrf_exempt
def check_endedmatch(request):
    # 날짜 셋팅
    now = datetime.datetime.now().time()
    # 알람이 생성되지 않은 매치: 경기가 끝나지 않은 매치들

    userMatches = (MatchInfo.objects.filter(is_alarmed=False) & MatchInfo.objects.filter(
        Q(host_id=request.user.pk) | Q(participant_id=request.user.pk)))
    print(userMatches.values())
    userMatches_json = []
    if len(userMatches) != 0:
        for match in userMatches:
            matchTime = match.end_time.replace(tzinfo=None)
            if matchTime < now:
                userMatches_json.append({
                    'match_id': match.id,
                    'host_teamname': match.host_id.team_name,
                    'participant_teamname': match.participant_id.team_name,
                    'end_time': match.end_time
                })
        # userMatches_json = json.loads(serializers.serialize(
        #     'json', userMatches))
        # userMatches_json = serializers.serialize(
        #     'json', userMatches_json)
    return JsonResponse({'userMatches': userMatches_json})




def endOfGame(request, *args, **kwargs):
    return render(request, "matchingMatch/endOfGame.html")



def login_page(request):
    page = 'login'

    if request.method == "POST":
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )

        if user is not None:
            login(request, user)
            messages.error(request, '성공적으로 로그인이 진행됐습니다.')
            return redirect('matchingMatch:main') 
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
            messages.error(request, '성공적으로 회원가입이 진행됐습니다.')
            return redirect('matchingMatch:main')
        else:
            messages.error(request, '회원가입 도중에 문제가 발생하였습니다.')

    page = 'register'
    context = {'page':page, 'form':form}
    return render(request, 'matchingMatch/login_register.html', context)


def logout_user(request):
    logout(request)
    messages.info(request, '로그아웃 상태입니다.')
    return redirect('matchingMatch:login')

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
    return render(request, 'matchingMatch/account.html', context)

@login_required(login_url='/login')
def change_password(request):   
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
      
        if password1 == password2:
            new_pass = make_password(password1)
            request.user.password = new_pass
            request.user.save()
            messages.success(request, '비밀번호를 성공적으로 변경하셨습니다!')
            return redirect('matchingMatch:account')
    return render(request, 'matchingMatch/change_password.html')
# 매치 상대방 평가하기

@login_required(login_url='/login')
def edit_account(request):

    form = UserForm(instance=request.user)

    if request.method == 'POST':
        #print('ORIGINAL Image', request.FILES.get('avatar'))
        # img = Image.open(request.FILES.get('avatar'))
        # newsize = (10, 10)
        # img = img.resize(newsize)
        # request.FILES['avatar'] = img
        # img = Image.open(user.avatar)
        # newsize = (10, 10)
        # img = img.resize(newsize)
        #print('NEW Image', request.FILES.get('avatar'))
        form = UserForm(request.POST, request.FILES,  instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('matchingMatch:account')

    context = {'form':form}
    return render(request, 'matchingMatch/user_form.html', context)

class delete_account(SuccessMessageMixin, generic.DeleteView):
  model = Team
  template_name = 'matchingMatch/delete_account_confirm.html'
  success_message = "유저가 성공적으로 삭제됐습니다."
  success_url = reverse_lazy('matchingMatch:main')

  
@csrf_exempt
def change_enroll(request):
  
  body_unicode = request.body.decode('utf-8')
  print(body_unicode)
  req = json.loads(body_unicode)
  
  match_id = int(req['id'])
  type =  req['type']
  
  
  #matchrequest 접근하는 방법
  # 1. 역참조
  # 2. get
  if type == "enroll-cancel":
    match_request = MatchRequest.objects.filter(match_id = match_id) & MatchRequest.objects.filter(team_id = request.user.pk)
    match_request.delete()
    type = "enroll"
  elif type == "enroll":
    type = "enroll-cancel"
    match = get_object_or_404(MatchInfo, id = match_id)
    MatchRequest.objects.create(team_id = request.user, match_id = match)
  else:
    # 잘못된 입력 예외처리
    ...
  
  return JsonResponse({'id' : match_id, "type" : type})
  
  
  


# 해당 pk에 해당하는 유저가 로그인 했을 때만 이 페이지가 보이게끔 만들어야됨.
@login_required(login_url='/login')
def my_register_matches(request, pk):  # pk는 team pk, 마이페이지에서 pk를 받아옴.
    my_not_matched_matches = MatchInfo.objects.filter(
        is_matched=False, host_id=pk)

    my_matched_matches = MatchInfo.objects.filter(is_matched=True, host_id=pk)
    context = {
        'my_not_matched_matches': my_not_matched_matches,
        'my_matched_matches' : my_matched_matches
    }
    return render(request, 'matchingMatch/my_register_matches.html', context=context)

@login_required()
def my_apply_matches(request, pk):



  my_matched_matches = MatchInfo.objects.filter(is_matched=True,participant_id=pk)
  my_match_requests = MatchRequest.objects.filter(team_id=pk)
  context = {
      'my_matched_matches' : my_matched_matches,
      'my_match_requests' :  my_match_requests,
  }
  return render(request, 'matchingMatch/my_apply_matches.html', context=context) 

@login_required(login_url='/login')
def applying_team_list(request, pk):  # pk는 매치 pk, 경기 정보 페이지(주최자)에서 받아옴
    if request.method == "POST":
      team = Team.objects.get(id=request.POST['select_participant'])
      match = MatchInfo.objects.get(id=pk)
      match.participant_id = team
      match.is_matched = True
      match.save()
      return redirect("/")
    applying_team_list = MatchRequest.objects.filter(match_id=pk)
    match = MatchInfo.objects.get(id=pk)
    context = {
        'applying_team_list' : applying_team_list,
        'match' : match
    }
    return render(request, 'matchingMatch/applying_team_list.html', context=context)

def rate(request, pk):
    if request.method == "POST":
        host = Team.objects.get(id=request.user.id)
        match = MatchInfo.objects.get(id=pk)
        match.is_alarmed = True
        participant = Team.objects.get(id=match.participant_id.id)
        host.match_count += 1
        participant.match_count += 1
        participant.level = (participant.level +
                             float(request.POST['level']))/participant.match_count
        participant.manner = (participant.manner +
                              float(request.POST['manner']))/participant.match_count
        match.save()
        host.save()
        participant.save()
        return redirect('/')




@login_required(login_url='/login')
@admin_required
#차단 유저 목록 
def admin_team_block(request):
  ...
#삭제 목록
def admin_match_delete(request):
  ...