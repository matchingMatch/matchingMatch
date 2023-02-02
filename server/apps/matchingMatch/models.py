from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
# Create your models here.

class Team(models.Model):
  team_name = models.CharField(null = False, max_length=20)
  team_logo = models.ImageField()
  team_intro = models.TextField(blank= True)
  region = models.CharField(max_length=20)
  photo = models.ImageField(null = True)
  manner = models.IntegerField(null = True, default = 0) # 지금까지 받은 매너 점수의 합
  level = models.IntegerField(null = True, default = 0) 
  match_count = models.PositiveIntegerField(default = 0)
  pre_proplayer = models.TextField(null = True) 
  

class User(AbstractUser, PermissionsMixin):
  team = models.ForeignKey(Team, on_delete= models.CASCADE, related_name = "user_team")

class Stadium(models.Model):
  stadium_name = models.CharField(max_length = 250, null = False)
  address = models.CharField(max_length = 250)
  is_park = models.BooleanField(default = 0, null = True)
  location = models.CharField(max_length = 10, null = False)

class MatchInfo(models.Model):

  gender_list = (("male", "남성"), ("female", "여성"), ("mixed", "혼성"))

  host_id = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="host_team")
  participant_id = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="participant_team")
  stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE, related_name="stadium")
  date = models.DateField(null = True, blank = True)
  is_matched = models.BooleanField(default = False, null = False)
  gender = models.CharField(choices=gender_list, max_length = 10, null = False)
  stadium_cost = models.CharField(max_length = 200, null = True)
  etc = models.CharField(max_length=200, null = True)
  start_time = models.DateTimeField()
  end_time = models.DateTimeField()





