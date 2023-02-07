import datetime
from django.shortcuts import render, redirect
from .models import MatchInfo, Alarm
from models import Team, MatchInfo, Stadium
from forms import MatchRegisterForm, TeamRegisterForm
from django.shortcuts import get_object_or_404
# Create your views here.



def match_detail(request, pk): # pk = 매치 아이디

  user = request.user

  match = get_object_or_404(MatchInfo, pk = pk)

  context = {"user" : user, "match" : match}

  return render(request, "html", context=context)



def team_detail(request, pk): # pk = 팀 아이디

  user = request.user

  match = get_object_or_404(Team, pk = pk)

  context = {"user" : user, "match" : match}

  return render(request, "html", context=context)




def team_update(request, pk):
  match = get_object_or_404(Team, pk = pk)
  if request.method == "POST":
    match_form = TeamRegisterForm(request.POST)
    if match_form.is_valid():
      match_form.save()
      return redirect("/")
    else:
      return render()
  else:
    match_form = TeamRegisterForm(instance=match)
    context = {"match_form" : match_form}

    return render(request, "html", context=context)



def my_page(request, pk): # pk = 유저 아이디
  #아직 어떤 기능을 넣을지 미정
  pass



def match_register(request):
  
  if request.method == "POST":
    match_form = MatchRegisterForm(request.POST)
    if match_form.is_valid():
      match_form.save()
      return redirect("/")
  
  match_form = MatchRegisterForm()
  context = {"match_form" : match_form}

  return render(request, "html", context=context)


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
    alarm = Alarm.objects.filter(team_id=request.user)
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
