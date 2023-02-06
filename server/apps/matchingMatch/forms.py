from django import forms
from models import MatchInfo


class MatchRegisterForm(forms.ModelForm):

  class Meta:
    model = MatchInfo
    field = []