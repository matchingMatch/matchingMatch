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
from django.core.paginator import Paginator
import os
from django.core.files import File
from django.core.files.storage import default_storage
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

    if team.match_count >= 3:
        level = team.level / team.match_count
        manner = team.manner / team.match_count
        level = round(level, 1)
        manner = round(manner, 1)
    else:
        level = None
        manner = None
    context = {"user": user, "team": team,
               "match_list": match_list, "level": level, "manner": manner}
    return render(request, "matchingMatch/team_detail.html", context=context)


def team_list(request):
    order = request.GET.get("order")
    search = request.GET.get("team_search")
    page = request.GET.get("page")

    # print(order)
    # if order:
    #     teams = Team.objects.order_by(order)
    #     paginator = Paginator(teams, 10)
    #     teams = paginator.get_page(page)
    # else:
    #     teams = Team.objects.all()
    #     paginator = Paginator(teams, 10)
    #     teams = paginator.get_page(page)
    # if search != None:
    #     if order:
    #         teams = Team.objects.order_by(order)
    #         teams = teams.filter(team_name__contains=search)
    #         paginator = Paginator(teams, 10)
    #         teams = paginator.get_page(page)
    #     else:
    #         teams = Team.objects.all()
    #         teams = teams.filter(team_name__contains=search)
    #         paginator = Paginator(teams, 10)
    #         teams = paginator.get_page(page)

    if search:
        teams = Team.objects.filter(team_name__contains=search)
    else:
        teams = Team.objects.all()
    if order:
        teams = teams.order_by(order)
    teams = teams.filter(is_superuser=False, is_staff=False)
    paginator = Paginator(teams, 10)
    teams = paginator.get_page(page)
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
            # 만들어진 페이지로 이동
            return redirect("matchingMatch:match_detail", pk=match.pk)
        else:
            print(match_form.errors)
            stadium_name = Stadium.objects.order_by('stadium_name')
            stadium_name_list = stadium_name
            context = {"match_form": match_form, "stadium_name": stadium_name,
                       "stadium_name_list": stadium_name_list, }
            return render(request, "matchingMatch/match_register.html", context=context)

    else:
        stadium_name = Stadium.objects.order_by('stadium_name')
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
            stadium_name_list = Stadium.objects.order_by('stadium_name')
            context = {"match_form": match_form, "match_stadium": match.stadium,
                       'stadium_name_list': stadium_name_list}
            # 잘못된 부분 수정 요청

            # 다시 작성하기
            return render(request, "matchingMatch/match_update.html", context)

    else:
        match_form = MatchRegisterForm(instance=match)
        # stadium = match_form.stadium
        # match_form.stadium = Stadium.objects.get(id=stadium)
        stadium_name_list = Stadium.objects.order_by('stadium_name')
        context = {"match_form": match_form, "match_stadium": match.stadium,
                   'stadium_name_list': stadium_name_list}
        return render(request, "matchingMatch/match_update.html", context=context)


def match_delete(request, pk):  # 매치 자체를 없애기 매치를 없애면 어떤 게 생기나?

    if request.method == "POST":
        match = get_object_or_404(MatchInfo, id=pk)
        match.delete()
        return redirect("/")


def main(request, *args, **kwargs):

    now_time = datetime.datetime.now().time()
    today = datetime.date.today()

    match_detail_category = {
        'gender': 'gender__in',
        'is_matched': 'is_matched__in',
        'region': 'stadium__location__in',
        'date': 'date__in'
    }
    date_val = ''
    filter_set = dict()
    for key, value in dict(request.GET).items():
        if key == 'date' and value:

            date_val = value[0]
            value[0] = datetime.datetime.strptime(value[0], '%Y-%m-%d').date()

        key = match_detail_category.get(key)
        filter_set[key] = value

    filter_form = MatchFilterForm()
    # html 태그 상의 name  : html 태그 상의 value
    if filter_set:
        filter_form = MatchFilterForm(request.GET)
        matches = MatchInfo.objects.filter(**filter_set)
        is_date_filter = request.GET.get('date', False)
        if is_date_filter:
            matches = matches.filter(date=today, start_time__gte = now_time)
    else:
        matches = MatchInfo.objects.filter(date=today, start_time__gte = now_time)

    context = {
        'matches': matches,
        'filter_form': filter_form,
        'date_val': date_val
    }
    return render(request, "matchingMatch/main.html", context=context)


@csrf_exempt
def check_endedmatch(request):
    # 날짜 셋팅
    now = datetime.datetime.now().time()
    today = datetime.date.today()
    # 알람이 생성되지 않은 매치: 경기가 끝나지 않은 매치들
    userMatches = (MatchInfo.objects.filter(host_id=request.user.id, participant_rated=False) & MatchInfo.objects.filter(is_matched=True)) | (MatchInfo.objects.filter(
        participant_id=request.user.id, host_rated=False) & MatchInfo.objects.filter(is_matched=True))
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

            return success(request, '로그인 되었습니다.', 'matchingMatch:main')
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
            return success(request, '성공적으로 회원가입이 완료되었습니다.', 'matchingMatch:main')
        else:
            return redirect('matchingMatch:register')
    page = 'register'
    context = {'page': page, 'form': form}
    return render(request, 'matchingMatch/login_register.html', context)


def success(request, message: str, url):
    messages.info(request, message)
    sys_messages = list(messages.get_messages(request))
    sys_message = sys_messages.pop()
    print(sys_message)
    context = {"message": sys_message, 'redirect_url': url}
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
        old_image = request.user.team_logo
        form = UserForm(request.POST, request.FILES,  instance=request.user)
        # 뭔가 새로운 파일 있는 경우에만 not False
        img = request.FILES.get('team_logo', False)
        # 수정사항이 존재하는 경우에만
        # if img:
        #   request.user.team_logo.url

        if form.is_valid():

            user = form.save(commit=False)
            user.save()
            # 로고도 upload_to 설정해서 중복 없애야 할듯
            if img:
                old_image.delete(save=False)

            return redirect('matchingMatch:account')
    else:

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

        ended_matches = []  # 경기 성사 후 종료된 매치
        not_started_matches = []  # 경기 성사 후 시작되지 않은 매치
        before_start_time = []  # 매칭 성사 되지 않은 매치 중에서 시작 시간이 지나지 않은 매치들

        for match in my_matched_matches:
            if match.date < today:
                ended_matches.append(match)
            elif match.date > today:
                not_started_matches.append(match)
            else:
                if match.end_time < now:
                    ended_matches.append(match)
                if match.start_time > now:
                    not_started_matches.append(match)

        for match in my_not_matched_matches:
            if (match.date > today) or (match.date == today and match.start_time > now):
                before_start_time.append(match)

        context = {
            'ended': ended_matches,  # 성사 후 종료
            'not_started': not_started_matches,  # 성사 후 시작 전
            'before_start': before_start_time,  # 성사 되기 전 경기 시작시간 전
        }
        return render(request, 'matchingMatch/my_register_matches.html', context=context)
    else:
        return redirect("/")


@login_required(login_url='/login')
def my_apply_matches(request, pk):
    if request.user.id == pk:
        if request.method == "POST":  # 매치 신청 취소 post
            request_object = get_object_or_404(
                MatchRequest, id=request.POST.get('request_object_id'))
            request_object.delete()
            return redirect(f"/my_apply_matches/{request.user.id}")
        else:
            today = datetime.date.today()
            now = datetime.datetime.now().time()

            my_matched_matches = MatchInfo.objects.filter(
                is_matched=True, participant_id=pk)
            my_match_requests = MatchRequest.objects.filter(team_id=pk)

            ended_matches = []  # 경기 성사 후 종료된 매치
            not_started_matches = []  # 경기 성사 후 시작하기 전 매치
            before_start_time = []  # 경기 시작시간 지나기 전 성사되지 않은 요청

            for match in my_matched_matches:
                if match.date < today:
                    ended_matches.append(match)
                elif match.date > today:
                    not_started_matches.append(match)
                else:
                    if match.end_time < now:
                        ended_matches.append(match)
                    if match.start_time > now:
                        not_started_matches.append(match)

            for requests in my_match_requests:
                if (requests.match_id.date > today) or (requests.match_id.date == today and requests.match_id.start_time > now):
                    before_start_time.append(requests)

            context = {
                'ended': ended_matches,
                'not_started': not_started_matches,
                'before_start': before_start_time,
            }
            return render(request, 'matchingMatch/my_apply_matches.html', context=context)
    else:
        return redirect("/")


@login_required(login_url='/login')
def applying_team_list(request, pk):  # pk는 매치 pk, 경기 정보 페이지(주최자)에서 받아옴
    match = get_object_or_404(MatchInfo, id=pk)
    if (request.user.id) == match.host_id.pk:
        if request.method == "POST":
            try:
                team = get_object_or_404(
                    Team, id=request.POST['select_participant'])
                match = get_object_or_404(MatchInfo, id=pk)
                match.participant_id = team
                match.is_matched = True
                match.save()
                return redirect(f"/my_register_matches/{match.host_id.id}")
            except:
                return redirect(f"/applying_team_list/{pk}")
        applying_team_list = MatchRequest.objects.filter(match_id=pk)
        match = get_object_or_404(MatchInfo, id=pk)
        context = {
            'applying_team_list': applying_team_list,
            'match': match
        }
        return render(request, 'matchingMatch/applying_team_list.html', context=context)
    else:
        return render("/")


def rate(request, pk):
    if request.method == "POST":
        user = request.user
        match = get_object_or_404(MatchInfo, id=pk)
        opponent = object()
        if user == match.host_id:
            opponent = get_object_or_404(Team, id=match.participant_id.id)
            match.participant_rated = True
        elif user == match.participant_id:
            opponent = get_object_or_404(Team, id=match.host_id.id)
            match.host_rated = True
            print('완료')

        user.match_count += 1
        opponent.match_count += 1
        try:
            opponent.level = opponent.level + int(request.POST['level'])
            opponent.manner = opponent.manner + int(request.POST['manner'])
            opponent.level = opponent.level + int(request.POST['level'])
            opponent.manner = opponent.manner + int(request.POST['manner'])
            match.save()
            user.save()
            opponent.save()
        except:
            pass
        return redirect('/')


@login_required(login_url='/login')
def notice_list(request):
    all_notices = Notice.objects.all()
    notices_objects = all_notices.order_by('-id')  # 최신 순으로 보여 주기 위해
    page = request.GET.get("page")
    paginator = Paginator(notices_objects, 10)  # 한 페이지당 10개의 공지사항을 보여줌
    notices = paginator.get_page(page)
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
    notice = get_object_or_404(Notice, id=pk)

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
        notice = get_object_or_404(Notice, id=pk)
        notice.delete()
        return redirect("matchingMatch:notice_list")


@login_required(login_url='/login')
def report_list(request):  # pk는 team pk
    if request.user.is_superuser == False and request.user.is_staff == False:
        team_id = request.user.id
        report_objects = Report.objects.filter(writer_id=team_id)
        all_reports = report_objects.order_by('-id')  # 최신순으로 보여주기 위해
    else:
        all_reports = Report.objects.order_by('-id')

    paginator = Paginator(all_reports, 10)  # 한 페이지에 10개씩 보여줌
    page = request.GET.get("page")
    reports = paginator.get_page(page)
    context = {
        'reports': reports,
    }
    return render(request, "matchingMatch/report_list.html", context=context)


@login_required(login_url='/login')
def report_create(request):  # pk는 team pk

    form = ReportForm()
    if request.method == "POST":
        form = ReportForm(request.POST, request.FILES)

        if form.is_valid():
            report = form.save(commit=False)
            report.writer_id = request.user
            report.save()
            return redirect("matchingMatch:report_detail", pk=report.pk)
        context = {
            'form': form,
        }
        return render(request, "matchingMatch/report_create.html", context=context)
    else:
        context = {
            'form': form,
        }
        return render(request, "matchingMatch/report_create.html", context=context)


@login_required(login_url='/login')
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

    report = get_object_or_404(Report, id=pk)
    if report.writer_id.id == request.user.id or request.user.is_superuser == True:
        if request.method == "POST":
            old_image = report.image
            form = ReportForm(request.POST, request.FILES, instance=report)
            img = request.FILES.get('image', False)
            if form.is_valid():
                # image_path = form.image.path
                # if os.path.exists(image_path):
                #     os.remove(image_path)
                form.save()

                return redirect('matchingMatch:report_detail', pk=pk)

        form = ReportForm(instance=report)
        context = {
            'form': form,
            'report': report
        }
        return render(request, "matchingMatch/report_update.html", context=context)
    else:
        return redirect("matchingMatch:report_list")


@login_required(login_url='/login')
def report_delete(request, pk):  # pk는 report pk
    report = get_object_or_404(Report, id=pk)
    if report.writer_id.id == request.user.id or request.user.is_superuser == True or request.user.is_staff:
        if request.method == "POST":
            report.delete()
            return redirect("matchingMatch:report_list")
    else:
        return redirect("/")


@login_required(login_url='/login')
def cancel_game(request, pk):  # pk는 match pk
    match = get_object_or_404(MatchInfo, id=pk)
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


@login_required(login_url='/login')
def rate_list(request, pk):  # pk는 team pk
    if request.user.id == pk:
        today = datetime.date.today()
        now = datetime.datetime.now().time()

        matches = MatchInfo.objects.filter(
            host_id=pk, is_matched=True, participant_rated=False)
        not_rated_matches_by_host = []  # host가 별점 안 매긴 매치들

        for match in matches:
            if (match.date < today) or (match.date == today and match.end_time < now):
                not_rated_matches_by_host.append(match)

        matches = MatchInfo.objects.filter(
            participant_id=pk, is_matched=True, host_rated=False)
        not_rated_matches_by_participant = []  # participant가 별점 안 매긴 매치들

        for match in matches:
            if (match.date < today) or (match.date == today and match.end_time < now):
                not_rated_matches_by_participant.append(match)

        context = {
            'not_rated_matches_by_host': not_rated_matches_by_host,
            'not_rated_matches_by_participant':  not_rated_matches_by_participant,
        }
        return render(request, "matchingMatch/rate_list.html", context=context)
    else:
        return redirect("/")


@login_required(login_url='/login')
def rate_match(request, pk):  # pk는 match pk
    match = get_object_or_404(MatchInfo, id=pk)
    if (request.user.id == match.participant_id.id) or (request.user.id == match.host_id.id):
        if request.method == "POST":
            try:
                if request.user.id == match.participant_id.id:  # 상대방 아이디가 접속한 경우, host를 평가해야 됨.
                    match.host_id.manner += request.POST.get('manner')
                    match.host_id.level += request.POST.get('level')
                    match.host_id.match_count += 1
                    match.host_rated = True
                    match.host_id.save()
                    match.save()
                    return redirect(f"/rate_list/{request.user.id}")
                else:  # 주최자 아이디가 접속한 경우, participant를 평가해야됨.
                    match.participant_id.manner += request.POST.get('manner')
                    match.participant_id.level += request.POST.get('level')
                    match.participant_id.match_count += 1
                    match.participant_rated = True
                    match.participant_id.save()
                    match.save()
                    return redirect(f"/rate_list/{request.user.id}")
            except:
                return redirect(f"/rate_match/{pk}")
        else:
            context = {
                'match': match,
            }
            return render(request, "matchingMatch/rate_match.html", context=context)
    else:
        return redirect("/")
