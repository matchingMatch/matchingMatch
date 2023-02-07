from django.shortcuts import render, redirect
from server.apps.matchingMatch.models import Team, MatchInfo, Stadium
from server.apps.matchingMatch.forms import MatchRegisterForm
from django.shortcuts import get_object_or_404
from django.http.request import HttpRequest
# Create your views here.



# def match_detail(request, pk): # pk = 매치 아이디

#   user = request.user

#   match = get_object_or_404(MatchInfo, pk = pk)

#   context = {"user" : user, "match" : match}

#   return render(request, "html", context=context)



# def team_detail(request, pk): # pk = 팀 아이디

#   user = request.user

#   match = get_object_or_404(Team, pk = pk)

#   context = {"user" : user, "match" : match}

#   return render(request, "html", context=context)




# def team_update(request, pk):
#   match = get_object_or_404(Team, pk = pk)
#   if request.method == "POST":
#     match_form = TeamRegisterForm(request.POST)
#     if match_form.is_valid():
#       match_form.save()
#       return redirect("/")
#     else:
#       return render()
#   else:
#     match_form = TeamRegisterForm(instance=match)
#     context = {"match_form" : match_form}

#     return render(request, "html", context=context)



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


# #매치 결정
# def match_resolve(request, pk): # pk = 매치 아이디
  
#   if request.method == "POST":
#     match = get_object_or_404(MatchInfo, id = pk)
#     match.participant_id = request.user.pk
#     match.is_matched = True
#     match.save()
#     return redirect("/")

#   return render(request, "html")

