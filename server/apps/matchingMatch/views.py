import datetime
from django.shortcuts import render, redirect
from .models import MatchInfo, Alarm
# Create your views here.


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
