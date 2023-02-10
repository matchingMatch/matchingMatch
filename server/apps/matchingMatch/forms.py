from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from server.apps.matchingMatch.models import MatchInfo, Team



class MatchRegisterForm(forms.ModelForm):
  
  class Meta:
    model = MatchInfo
    fields = ['stadium','date','gender','stadium_cost','etc','start_time','end_time']

# 수정할 때만 사용되는 폼
# class TeamRegisterForm(UserCreationForm):
  
#   class Meta:
#     model = Team
#     fiedl = []

class UserForm(ModelForm):
    class Meta:
        model = Team
        fields = ['username', 'email', 'team_name', 'team_logo', 'team_intro', 'region', 'photo', 'pre_proplayer']
        labels = {
            'username': '유저네임',
            'team_name': '팀 이름',
            'team_logo': '팀 로고 (이미지 첨부파일)',
            'team_intro': '팀 소개',
            'region': '지역',
            'photo': '팀 사진 (이미지 첨부파일)',
            'pre_proplayer': '선출 수 (자세하게 적어주세요.)',
        }

class CustomUserCreateForm(UserCreationForm):
    class Meta:
        model = Team
        fields = ['username', 'email', 'password1', 'password2', 'team_name', 'team_logo', 'team_intro', 'region', 'photo', 'pre_proplayer']
        labels = {
            'username': '유저네임',
            'team_name': '팀 이름',
            'team_logo': '팀 로고 (이미지 첨부파일)',
            'team_intro': '팀 소개',
            'region': '지역',
            'photo': '팀 사진 (이미지 첨부파일)',
            'pre_proplayer': '선출 수 (자세하게 적어주세요.)',
        }