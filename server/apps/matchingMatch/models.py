from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from PIL import Image
from django.contrib.auth.validators import UnicodeUsernameValidator
# Create your models here.

USERNAME_FIELD = 'username'
class Team(AbstractUser, PermissionsMixin):
    team_name = models.CharField(null=False, max_length=20)
    team_logo = models.ImageField(blank=True, null=True, upload_to='posts/%Y%m%d')
    team_intro = models.TextField(blank=True)  # 팀소개
    region = models.CharField(max_length=20)
    photo = models.ImageField(blank=True, null=True, upload_to='posts/%Y%m%d')
    manner = models.IntegerField(null=True, default=0)  # 지금까지 받은 매너 점수의 합
    level = models.IntegerField(null=True, default=0)
    match_count = models.PositiveIntegerField(default=0)
    pre_proplayer = models.TextField(null=True)
    


class Stadium(models.Model):

    stadium_name = models.CharField(max_length=250, null=False)
    address = models.CharField(max_length=250)
    is_park = models.BooleanField(default=0, null=True)
    location = models.CharField(max_length=10, null=False)
    def __str__(self):
        return self.stadium_name

class MatchInfo(models.Model):
    gender_list = (("male", "남성"), ("female", "여성"), ("mixed", "혼성"))
    host_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="host_team")
    participant_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.CASCADE,
        related_name="participant_team")
    stadium = models.ForeignKey(
        Stadium, on_delete=models.CASCADE, related_name="stadium")
    date = models.DateField(null=True, blank=True)
    is_matched = models.BooleanField(
        default=False, null=False)  # 매치성사여부(매치종료여부는 아님)
    gender = models.CharField(choices=gender_list, max_length=10, null=False)
    stadium_cost = models.CharField(max_length=200, null=True)
    etc = models.CharField(max_length=200, null=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_alarmed = models.BooleanField(default=False)
    


class Alarm(models.Model):
    # Review : MatchInfo와 Alarm의 관계가 완벽히 정의된 것 같지 않습니다.
    # Review : MatchInfo.is_alarmed와 Alarm이 중복되는 것 같습니다.
    team_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="team_alarm")
    match_id = models.ForeignKey(
        MatchInfo, on_delete=models.CASCADE, related_name="designated_match")


class MatchRequest(models.Model):
    match_id = models.ForeignKey(
        MatchInfo, on_delete=models.CASCADE, related_name="request_match")
    team_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="request_team")