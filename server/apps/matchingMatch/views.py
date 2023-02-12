import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import render, redirect
from .forms import CustomUserCreateForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .forms import MatchRegisterForm
from .models import Team, MatchInfo, Stadium, Alarm
from django.db.models import Q
import datetime
# Create your views here.


def match_detail(request, pk):  # pk = 매치 아이디

    user = request.user

    match = get_object_or_404(MatchInfo, pk=pk)

    context = {"user": user, "match": match}

    return render(request, "html", context=context)


def team_detail(request, pk):  # pk = 팀 아이디

    user = request.user

    match = get_object_or_404(Team, pk=pk)

    context = {"user": user, "match": match}

    return render(request, "html", context=context)


def team_update(request, pk):
    match = get_object_or_404(Team, pk=pk)
    if request.method == "POST":
        match_form = CustomUserCreateForm(request.POST)
        if match_form.is_valid():
            match_form.save()
            return redirect("/")
        else:
            return render()
    else:
        match_form = CustomUserCreateForm(instance=match)
        context = {"match_form": match_form}

        return render(request, "html", context=context)


def my_page(request, pk):  # pk = 유저 아이디
    # 아직 어떤 기능을 넣을지 미정
    pass


def match_register(request):

    if request.method == "POST":
        match_form = MatchRegisterForm(request.POST)
        if match_form.is_valid():
            match_form.save()
            return redirect("/")

    match_form = MatchRegisterForm()
    context = {"match_form": match_form}

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
            return redirect("/")  # 수정된 페이지로 이동

        else:
            return redirect("/")  # 다시 작성하기

    else:
        match_form = MatchRegisterForm()
        context = {"match_form": match_form}
        return render(request, "html", context=context)


# 매치 결정
def match_resolve(request, pk):  # pk = 매치 아이디

    if request.method == "POST":
        match = get_object_or_404(MatchInfo, id=pk)
        match.participant_id = request.user.pk
        match.is_matched = True
        match.save()
        return redirect("/")

    return render(request, "html")


def main(request, *args, **kwargs):
    matches = MatchInfo.objects.filter(is_matched=False)
    userMatches = (MatchInfo.objects.filter(is_alarmed=False) & MatchInfo.objects.filter(
        Q(host_id=request.user.pk) | Q(participant_id=request.user.pk)))
    context = {
        'matches': matches,
        'userMatches': userMatches,

    }
    return render(request, "matchingMatch/main.html", context=context)


@csrf_exempt
def check_endedmatch(request):
    # 날짜 셋팅
    now = datetime.datetime.now()
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

    context = {'page': page}
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
    context = {'page': page, 'form': form}
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

    context = {'user': user}
    return render(request, 'account.html', context)

# 매치 상대방 평가하기


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
