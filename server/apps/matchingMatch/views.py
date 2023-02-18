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
from django.db.models import Q
from .models import Team, MatchInfo, Stadium, MatchRequest, Notice, Report
from .forms import CustomUserCreateForm, UserForm, NoticeForm, ReportForm, MatchFilterForm
from .decorator import admin_required, check_recaptcha
from django.conf import settings
import re
import datetime
import json
import requests
# Create your views here.


def match_detail(request, pk):  # pk = 매치 아이디
    team = request.user
    match = get_object_or_404(MatchInfo, pk=pk)

    # 매치 주최자가 현재 로그인 한 유저가 아닌 경우
    if team != match.host_id:
        # 역참조

        match_requests = MatchRequest.objects.filter(
            match_id=pk, team_id=team.id)

        if len(match_requests) == 0:
            context = {
                "user": team,
                "match": match,
                "status": 0
            }
        else:
            context = {
                "user": team,
                "match": match,
                "status": 1
            }
    else:
        context = {
            "user": team,
            "match": match,
            "status": 0,
        }

    return render(request, "matchingMatch/match_detail.html", context=context)


def team_detail(request, pk):  # pk = 팀 아이디
    user = request.user

    team = get_object_or_404(Team, id=pk)
    match_list = MatchInfo.objects.filter(host_id=team)
    context = {"user": user, "team": team, "match_list": match_list}

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
        teams = teams.filter(team_name__contains=search)
    # order와 search가 동시에 존재하는 경우?
    context = {"teams": teams,
               "order": order}
    return render(request, "matchingMatch/team_list.html", context=context)


@check_recaptcha
@login_required(login_url='/login')
def match_register(request):

    if request.method == "POST":
        match_form = MatchRegisterForm(request.POST, request.FILES)
        if match_form.is_valid() and request.recaptcha_is_valid:
            match = match_form.save(commit=False)
            match.host_id = request.user
            match.save()
            return redirect("/")
        else:
            stadium_name = Stadium.objects.all()
            stadium_name_list = stadium_name
            context = {"match_form": match_form, "stadium_name": stadium_name,
                       "stadium_name_list": stadium_name_list, }
            return render(request, "matchingMatch/match_register.html", context=context)

    else:
        stadium_name = Stadium.objects.all()
        stadium_name_list = stadium_name
        match_form = MatchRegisterForm()
        context = {"match_form": match_form, "stadium_name": stadium_name,
                   "stadium_name_list": stadium_name_list, }

        return render(request, "matchingMatch/match_register.html", context=context)


@csrf_exempt
def match_cancel(request):  # 매치 신청 취소
    body_unicode = request.body.decode('utf-8')

    req = json.loads(body_unicode)
    match_request = get_object_or_404(MatchRequest, team_id=req['team.id'])

    match_request.delete()

    status = not req['status']

    return JsonResponse({'status': status})


@csrf_exempt
def match_request(request):  # 매치 신청
    body_unicode = request.body.decode('utf-8')

    req = json.loads(body_unicode)

    MatchRequest.objects.create(
        match_id=req['match.id'], team_id=req['team.id'])
    status = not req['status']

    return JsonResponse({'status': status})


@login_required(login_url='/login')
def match_update(request, pk):
    match = get_object_or_404(MatchInfo, id=pk)
    if request.method == "POST":
        print(match.id)
        match_form = MatchRegisterForm(request.POST, instance=match)
        if match_form.is_valid():
            match = match_form.save(commit=False)
            match.save()
            return redirect("matchingMatch:match_detail", pk=pk)  # 수정된 페이지로 이동

        else:
            context = {"match_form": match_form, "match_stadium" : match.stadium}
            # 잘못된 부분 수정 요청

            # 다시 작성하기
            return render(request, "matchingMatch/match_update.html", context)

    else:
        match_form = MatchRegisterForm(instance=match)
        # stadium = match_form.stadium
        # match_form.stadium = Stadium.objects.get(id=stadium)
        context = {"match_form": match_form, "match_stadium" : match.stadium}
        return render(request, "matchingMatch/match_update.html", context=context)


def match_delete(request, pk):  # 매치 자체를 없애기 매치를 없애면 어떤 게 생기나?

    if request.method == "POST":
        match = get_object_or_404(MatchInfo, id=pk)
        match.delete()
        return redirect("/")


# team detail과 다른 점?
def my_page(request, pk):  # pk = 유저 아이디
    # 아직 어떤 기능을 넣을지 미정
    pass


def main(request, *args, **kwargs):

    match_detail_category = {
        'gender': 'gender__in',
        'is_matched': 'is_matched__in',
        'region': 'stadium__location__in',
        'date' : 'date__in'
    }
    date_val = ''
    filter_set = dict()
    for key, value in dict(request.GET).items():
        if key == 'date' and value:
            date_val = value[0]
            value[0] = datetime.datetime.strptime(value[0], '%Y-%m-%d').date()

        key = match_detail_category.get(key)
        filter_set[key] = value
    print(date_val)
    
    filter_form = MatchFilterForm()
    # html 태그 상의 name  : html 태그 상의 value
    if filter_set:
        

        filter_form = MatchFilterForm(request.GET)
        matches = MatchInfo.objects.filter(**filter_set)

    else:
        matches = MatchInfo.objects.all()
    
    now_time = datetime.datetime.now().time()
    today = datetime.date.today()

    matches = matches.filter(date = today, start_time__gte = now_time) | matches.filter(date__gt = today)
    
    
    context = {
        'matches': matches,
        'filter_form' : filter_form,
        'date_val' : date_val
        }
    return render(request, "matchingMatch/main.html", context=context)


@csrf_exempt
def check_endedmatch(request):
    # 날짜 셋팅
    now = datetime.datetime.now().time()
    today = datetime.date.today()
    # 알람이 생성되지 않은 매치: 경기가 끝나지 않은 매치들

    userMatches = (MatchInfo.objects.filter(host_id=request.user.id, participant_rated=False) & MatchInfo.objects.exclude(participant_id=None)) | MatchInfo.objects.filter(
        participant_id=request.user.id, host_rated=False)
    userMatches_json = []
    if len(userMatches) != 0:
        for match in userMatches:
            matchTime = match.end_time.replace(tzinfo=None)
            if matchTime < now and match.date <= today:
                userMatches_json.append({
                    'match_id': match.id,
                    'host_teamname': match.host_id.team_name,
                    'participant_teamname': match.participant_id.team_name,
                    'end_time': match.end_time
                })
    print(userMatches_json)
    return JsonResponse({'userMatches': userMatches_json})


def login_page(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )

        if user is not None:
            login(request, user)

            return success(request, '로그인 되었습니다.')
        else:
            messages.error(request, '이메일 혹은 비밀번호를 다시 확인해주세요.')
            return redirect('matchingMatch:login')

    context = {'page': page}
    return render(request, 'matchingMatch/login_register.html', context)


@check_recaptcha
def register_page(request):
    form = CustomUserCreateForm()
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == 'POST':
        form = CustomUserCreateForm(request.POST, request.FILES,)
        if form.is_valid() and request.recaptcha_is_valid:
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return success(request, '성공적으로 회원가입이 완료되었습니다.')
        else:
            return redirect('matchingMatch:register')
    page = 'register'
    context = {'page': page, 'form': form}
    return render(request, 'matchingMatch/login_register.html', context)


def success(request, message:str):
    messages.info(request, message)
    sys_messages = list(messages.get_messages(request))
    sys_message = sys_messages.pop()
    print(sys_message)
    context = {"message": sys_message}
    return render(request, "matchingMatch/register_success.html", context)


def logout_user(request):
    if request.user.is_authenticated:

        logout(request)
    return redirect('matchingMatch:main')


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
        # print('ORIGINAL Image', request.FILES.get('avatar'))
        # img = Image.open(request.FILES.get('avatar'))
        # newsize = (10, 10)
        # img = img.resize(newsize)
        # request.FILES['avatar'] = img
        # img = Image.open(user.avatar)
        # newsize = (10, 10)
        # img = img.resize(newsize)
        # print('NEW Image', request.FILES.get('avatar'))
        form = UserForm(request.POST, request.FILES,  instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('matchingMatch:account')

    context = {'form': form}
    return render(request, 'matchingMatch/user_form.html', context)


class delete_account(SuccessMessageMixin, generic.DeleteView):
    model = Team
    template_name = 'matchingMatch/delete_account_confirm.html'
    success_message = "유저가 성공적으로 삭제됐습니다."
    success_url = reverse_lazy('matchingMatch:main')


@login_required(login_url='/login')
@csrf_exempt
def change_enroll(request):

    body_unicode = request.body.decode('utf-8')
    print(body_unicode)
    req = json.loads(body_unicode)

    match_id = int(req['id'])
    type = req['type']

    # matchrequest 접근하는 방법
    # 1. 역참조
    # 2. get
    if type == "enroll-cancel":
        match_request = MatchRequest.objects.filter(
            match_id=match_id) & MatchRequest.objects.filter(team_id=request.user.pk)
        match_request.delete()
        type = "enroll"
    elif type == "enroll":
        type = "enroll-cancel"
        match = get_object_or_404(MatchInfo, id=match_id)
        MatchRequest.objects.create(team_id=request.user, match_id=match)
    else:
        # 잘못된 입력 예외처리
        ...

    return JsonResponse({'id': match_id, "type": type})


# 해당 pk에 해당하는 유저가 로그인 했을 때만 이 페이지가 보이게끔 만들어야됨.
@login_required(login_url='/login')
def my_register_matches(request, pk):  # pk는 team pk, 마이페이지에서 pk를 받아옴.
    if request.user.id == pk:
        today = datetime.date.today()
        now = datetime.datetime.now().time()

        my_matched_matches = MatchInfo.objects.filter(
            is_matched=True, host_id=pk)
        my_not_matched_matches = MatchInfo.objects.filter(
            is_matched=False, host_id=pk)

        ended_matches = []
        ended_yet_matches = []

        for match in my_matched_matches:
            if match.date < today:
                ended_matches.append(match)
            elif match.date > today:
                ended_yet_matches.append(match)
            elif match.start_time < now:
                ended_matches.append(match)

        context = {
            'ended': ended_matches,
            'ended_yet': ended_yet_matches,
            'my_not_matched_matches': my_not_matched_matches,
        }
        return render(request, 'matchingMatch/my_register_matches.html', context=context)
    else:
        return redirect("/")


@login_required(login_url='/login')
def my_apply_matches(request, pk):
    if request.user.id == pk:
        if request.method == "POST":
            request_object = MatchRequest.objects.get(id=request.POST.get('request_object_id'))
            request_object.delete()
            return redirect(f"/my_apply_matches/{request.user.id}")
        else:
            today = datetime.date.today()
            now = datetime.datetime.now().time()

            my_matched_matches = MatchInfo.objects.filter(
                is_matched=True, participant_id=pk)
            ended_matches = []
            ended_yet_matches = []

            for match in my_matched_matches:
                if match.date < today:
                    ended_matches.append(match)
                elif match.date > today:
                    ended_yet_matches.append(match)
                elif match.start_time < now:
                    ended_matches.append(match)
            my_match_requests = MatchRequest.objects.filter(team_id=pk)
            context = {
                'ended': ended_matches,
                'ended_yet': ended_yet_matches,
                'my_match_requests':  my_match_requests,
            }
            return render(request, 'matchingMatch/my_apply_matches.html', context=context)
    else:
        return redirect("/")


@login_required(login_url='/login')
def applying_team_list(request, pk):  # pk는 매치 pk, 경기 정보 페이지(주최자)에서 받아옴
    match = MatchInfo.objects.get(id=pk)
    if (request.user.id) == match.host_id.pk:
        if request.method == "POST":
            try:
                team = Team.objects.get(id=request.POST['select_participant'])
                match = MatchInfo.objects.get(id=pk)
                match.participant_id = team
                match.is_matched = True
                match.save()
                return redirect(f"/my_register_matches/{match.host_id.id}")
            except:
                return redirect(f"/applying_team_list/{pk}")
        applying_team_list = MatchRequest.objects.filter(match_id=pk)
        match = MatchInfo.objects.get(id=pk)
        context = {
            'applying_team_list': applying_team_list,
            'match': match
        }
        return render(request, 'matchingMatch/applying_team_list.html', context=context)
    else:
        return render("/")


def rate(request, pk):
    if request.method == "POST":
        user = Team.objects.get(id=request.user.id)
        match = MatchInfo.objects.get(id=pk)
        opponent = object()
        if user == match.host_id:
            opponent = Team.objects.get(id=match.participant_id.id)
            match.participant_rated = True
        else:
            opponent = Team.objects.get(id=match.host_id.id)
            match.host_rated = True

        user.match_count += 1
        opponent.match_count += 1
        try:
            opponent.level = opponent.level + float(request.POST['level'])
            opponent.manner = opponent.manner + float(request.POST['manner'])
            match.save()
            user.save()
            opponent.save()
        except:
            pass
        return redirect('/')


@login_required(login_url='/login')
@admin_required
# 차단 유저 목록
def admin_team_block(request):
    blocked_teams = Team.objects.filter(is_active=False)

    return render("admin_block")
# 삭제 목록


def admin_match_delete(request):
    ...


@login_required(login_url='/login')
def notice_list(request):
    notices = Notice.objects.all()
    context = {
        'notices': notices,
    }
    return render(request, "matchingMatch/notice_list.html", context=context)


@login_required(login_url='/login')
def notice_detail(request, pk):
    notice = get_object_or_404(Notice, id=pk)
    context = {
        'notice': notice,
    }
    return render(request, "matchingMatch/notice_detail.html", context=context)


@login_required(login_url='/login')
@admin_required
def notice_create(request):
    form = NoticeForm()

    if request.method == "POST":
        form = NoticeForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect("matchingMatch:notice_list")
    context = {
        'form': form,
    }
    return render(request, "matchingMatch/notice_create.html", context=context)


@login_required(login_url='/login')
@admin_required
def notice_update(request, pk):
    notice = Notice.objects.get(id=pk)

    if request.method == "POST":
        form = NoticeForm(request.POST, instance=notice)
        if form.is_valid:
            notice = form.save(commit=False)
            notice.writer = request.POST['writer']
            notice.title = request.POST['title']
            notice.content = request.POST['content']
            notice.save()
            return redirect(f"/notice_detail/{pk}")

    form = NoticeForm(instance=notice)
    context = {
        'form': form,
        'notice': notice
    }
    return render(request, "matchingMatch/notice_update.html", context=context)


@login_required(login_url='/login')
@admin_required
def notice_delete(request, pk):
    if request.method == "POST":
        notice = Notice.objects.get(id=pk)
        notice.delete()
        return redirect("matchingMatch:notice_list")


@login_required(login_url='/login')
def report_list(request, pk):  # pk는 team pk
    if (request.user.id) == pk or (request.user.is_superuser) == True:
        team = Team.objects.get(id=pk)
        reports = Report.objects.filter(writer_id=team)
        context = {
            'reports': reports,
            'team': team,
        }
        return render(request, "matchingMatch/report_list.html", context=context)
    else:
        return redirect("/")


@login_required(login_url='/login')
def report_create(request, pk):  # pk는 team pk
    if (request.user.id) == pk:
        form = ReportForm()

        if request.method == "POST":
            form = ReportForm(request.POST, request.FILES)
            team = Team.objects.get(id=pk)
            if form.is_valid:
                report = form.save()
                report.writer_id = team
                report.save()
                return redirect(f"/report_list/{pk}")

        team = Team.objects.get(id=pk)
        context = {
            'form': form,
            'team': team,
        }
        return render(request, "matchingMatch/report_create.html", context=context)
    else:
        return redirect("/")


@login_required
def report_detail(request, pk):  # pk는 report pk
    report = get_object_or_404(Report, id=pk)
    if report.writer_id.id == request.user.id or request.user.is_superuser == True:
        context = {
            'report': report,
        }
        return render(request, "matchingMatch/report_detail.html", context=context)
    else:
        return redirect("/")


@login_required(login_url='/login')
def report_update(request, pk):  # pk는 report pk

    report = Report.objects.get(id=pk)
    if report.writer_id.id == request.user.id or request.user.is_superuser == True:
        if request.method == "POST":
            form = ReportForm(request.POST, request.FILES, instance=report)
            if form.is_valid():
                # image_path = form.image.path
                # if os.path.exists(image_path):
                #     os.remove(image_path)
                form.save()
                return redirect(f"/report_detail/{pk}")

        form = ReportForm(instance=report)
        context = {
            'form': form,
            'report': report
        }
        return render(request, "matchingMatch/report_update.html", context=context)
    else:
        return redirect("/")


@login_required(login_url='/login')
def report_delete(request, pk):  # pk는 report pk
    report = Report.objects.get(id=pk)
    if report.writer_id.id == request.user.id or request.user.is_superuser == True:
        if request.method == "POST":
            report.delete()
            return redirect(f"/report_list/{request.user.id}")
    else:
        return redirect("/")


@login_required(login_url='/login')
def cancel_game(request, pk):  # pk는 match pk
    match = MatchInfo.objects.get(id=pk)
    if request.user.id == match.host_id.id or request.user.id == match.participant_id.id:
        if request.method == "POST":
            match_requests_filter = MatchRequest.objects.filter(
                team_id=match.participant_id, match_id=match)
            match_requests_filter[0].delete()  # 신청 내역 삭제
            match.is_matched = False
            match.participant_id = None
            match.save()
            if request.user.id == match.host_id.id:
                return redirect(f"/my_register_matches/{request.user.id}")
            else:
                return redirect(f"/my_apply_matches/{request.user.id}")
    else:
        return redirect("/")
