from django import forms
from server.apps.matchingMatch.models import MatchInfo


class MatchRegisterForm(forms.ModelForm):
  
  class Meta:
    model = MatchInfo
    field = ['stadium','date', 'gender','stadium_cost','start_time','end_time']