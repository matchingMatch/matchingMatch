from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Team
from django import forms

class CustomUserCreateForm(UserCreationForm):
    class Meta:
        model = Team
        fields = ['username', 'email', 'password1', 'password2', 'team_name', 'team_logo', 'team_intro', 'region', 'photo', 'pre_proplayer']