from django import forms
from django.contrib.auth.forms import UserCreationForm
from models import MatchInfo, Team



class MatchRegisterForm(forms.ModelForm):
  
  class Meta:
    model = MatchInfo
    field = []


class TeamRegisterForm(UserCreationForm):
  
  class Meta:
    model = Team
    fiedl = []
