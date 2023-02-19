from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from PIL import Image
from django.contrib.auth.validators import UnicodeUsernameValidator
from server.config.utils import image_resize
from django.db.models.signals import post_delete
from django.dispatch import receiver

# Create your models here.
# Team 모델에 modes.Model이 없어서 역참조가 안됨
USERNAME_FIELD = 'username'


class Team(AbstractUser, PermissionsMixin):

    gender_list = (("male", "남성"), ("female", "여성"), ("mixed", "혼성"))
    team_name = models.CharField(null=False, max_length=20)
    team_logo = models.ImageField(
        blank=True, null=True, default='avatar.png', upload_to = 'logo/%Y%m%d') #upolad_to 설정하는 게 좋아보임
    team_intro = models.TextField(blank=True)  # 팀소개
    region = models.CharField(max_length=20)
    photo = models.ImageField(blank=True, null=True, upload_to='posts/%Y%m%d')
    manner = models.IntegerField(null=True, default=0)  # 지금까지 받은 매너 점수의 합
    level = models.IntegerField(null=True, default=0)
    match_count = models.PositiveIntegerField(default=0)
    gender = models.CharField(choices=gender_list, max_length=10, null=False)
    pre_proplayer = models.TextField(null=True)

    def save(self, commit=True, *args, **kwargs):
        if commit:
            image_resize(self.team_logo, 150, 150)
            super().save(*args, **kwargs)


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
    date = models.DateField(null=False, blank=False)
    is_matched = models.BooleanField(
        default=False, null=False)  # 매치성사여부(매치종료여부는 아님)
    gender = models.CharField(choices=gender_list, max_length=10, null=False)
    stadium_cost = models.CharField(max_length=200, null=True)
    etc = models.CharField(max_length=200, null=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    host_rated = models.BooleanField(default=False)
    participant_rated = models.BooleanField(default=False)



class MatchRequest(models.Model):
    match_id = models.ForeignKey(
        MatchInfo, on_delete=models.CASCADE, related_name="request_match")
    team_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="request_team")


class Notice(models.Model):
    title = models.CharField(max_length=128)
    writer = models.CharField(max_length=32)
    content = models.TextField()
    hits = models.PositiveIntegerField(default=0)  # 조회수
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def hits_counter(self):
        self.hits = self.hits + 1
        self.save()


class Report(models.Model):
    title = models.CharField(max_length=128)
    writer = models.CharField(max_length=32)
    writer_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, related_name="writer_id")
    content = models.TextField()
    image = models.ImageField(blank=True, null=True, upload_to='posts/%Y%m%d')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
