from django import forms
from django.contrib.auth.forms import UserCreationForm
from server.apps.matchingMatch.models import MatchInfo, Team



class MatchRegisterForm(UserCreationForm):
  
  class Meta:
    model = MatchInfo
    fields = ['stadium','date','gender','stadium_cost','etc','start_time','end_time']


# class TeamRegisterForm(UserCreationForm):
  
#   class Meta:
#     model = Team
#     fiedl = []
