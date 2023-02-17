from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from server.apps.matchingMatch.models import MatchInfo, Team, Notice, Report, Stadium



class MatchRegisterForm(forms.ModelForm):

  class Meta:
    model = MatchInfo
    fields = ['stadium','date','gender','stadium_cost','etc','start_time','end_time']
    labels = {
        'stadium' : '축구장',
        'date' : '날짜',
        'gender' : '설명',
        'stadium_cost' : '원구장비',
        'etc' : '기타사항',
        'start_time' : '시작 시간',
        'end_time' : '종료 시간',
    }
    
    widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}, ),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }


class UserForm(ModelForm):
    class Meta:
        model = Team
        fields = ['username', 'email', 'team_name', 'team_logo', 'team_intro', 'region', 'photo', 'gender', 'pre_proplayer']
        labels = {
            'username': '유저네임',
            'team_name': '팀 이름',
            'team_logo': '팀 로고 (이미지 첨부파일)',
            'team_intro': '팀 소개',
            'region': '지역',
            'photo': '팀 사진 (이미지 첨부파일)',
            'gender': '팀 성별',
            'pre_proplayer': '선출 수 (자세하게 적어주세요.)',
        }

class CustomUserCreateForm(UserCreationForm):
    class Meta:
        model = Team
        fields = ['username', 'email', 'password1', 'password2', 'team_name', 'team_logo', 'team_intro', 'region', 'photo', 'gender', 'pre_proplayer']
        labels = {
            'username': '유저네임',
            'team_name': '팀 이름',
            'team_logo': '팀 로고 (이미지 첨부파일)',
            'team_intro': '팀 소개',
            'region': '지역',
            'photo': '팀 사진 (이미지 첨부파일)',
            'gender': '팀 성별',
            'pre_proplayer': '선출 수 (자세하게 적어주세요.)',
        }

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'writer', 'content']
        labels = {
            'title' : '제목',
            'writer' : '작성자',
            'content' : '내용',
        }

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['title', 'writer', 'content','image']
        labels = {
            'title' : '제목',
            'writer' : '작성자',
            'content' : '내용',
            'image' : '첨부 이미지',
        }


is_matched_list = [(True and False, "전체"), (False, "모집중"), (True, "마감됨")]

class MatchFilterForm(forms.ModelForm):
    region = forms.ModelChoiceField(Stadium.objects.values_list('location', flat=True).distinct(), empty_label=None, widget=forms.CheckboxSelectMultiple)
    is_matched = forms.ChoiceField(choices=is_matched_list)
    class Meta:
        model = MatchInfo
        fields = ['is_matched', 'region', 'gender']
        labels = {
        "region" : "지역",
        'is_matched' : '마감여부',
        'gender' : '성별',
        }
        