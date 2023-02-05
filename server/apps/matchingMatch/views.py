import datetime
from django.shortcuts import render, redirect
from .models import MatchInfo
# Create your views here.


def main(request, *args, **kwargs):
    return render(request, "matchingMatch/main.html")


def endOfGame(request, *args, **kwargs):
    return render(request, "matchingMatch/endOfGame.html")


def check_endOfGame(request, *args, **kwargs):
    # 날짜 셋팅
    now = datetime.datetime.now()
    endOfGame = False
    MatchInfos = MatchInfo.objects.all()
    print(MatchInfos)

    if len(MatchInfos) != 0:
        for match in MatchInfos:
            matchTime = match.end_time
            if matchTime < now:
                print(matchTime)
                print(now)
                endOfGame = True
                return render(request, "matchingMatch/endOfGame.html", {'endOfGame': endOfGame})
