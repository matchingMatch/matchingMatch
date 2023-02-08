from django import forms
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

class CustomUserCreateForm(UserCreationForm):
    class Meta:
        model = Team
        fields = ['username', 'email', 'password1', 'password2', 'team_name', 'team_logo', 'team_intro', 'region', 'photo', 'pre_proplayer']