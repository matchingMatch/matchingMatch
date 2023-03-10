from django import forms
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from server.apps.matchingMatch.models import MatchInfo, Team, Notice, Report, Stadium
import datetime






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
                'stadium' : forms.TextInput(attrs={
                        'id' :"stadium_search",
	    				'list' :"stadium_list",
	    				'placeholder' : "축구장 검색"}),
                'start_time': forms.TimeInput(attrs={'type': 'time'}, ),
                'end_time': forms.TimeInput(attrs={'type': 'time'}),
            }
            
    def clean(self):
        clean_data = super().clean()
        start_time = self.cleaned_data.get('start_time', False)
        end_time = self.cleaned_data.get('end_time', False)
        date = self.cleaned_data.get('date', False)
        now_date = datetime.date.today()
        if not start_time or  not  end_time or not date:
            return clean_data 
        if start_time > end_time:
            raise ValidationError({'start_time': "종료시간이 시작시간보다 이릅니다"}, code = 'invalid')
        
        elif date < now_date or (date == now_date and datetime.datetime.now().time()> start_time):
            raise ValidationError({"date": "현재시간이 시작시간보다 이릅니다"},
                code='invalid'
            )
        return clean_data
      


class UserForm(ModelForm):
    class Meta:
        model = Team
        fields = ['username', 'email', 'team_name', 'team_logo', 'team_intro', 'region', 'photo', 'gender', 'pre_proplayer']
        labels = {
            'username': '아이디',
            'email': '이메일',
            'team_name': '팀 이름',
            'team_logo': '팀 로고 (이미지 첨부파일)',
            'team_intro': '팀 소개 (자세하게 적어주세요.)',
            'region': '지역',
            'photo': '팀 사진 (이미지 첨부파일)',
            'gender': '팀 성별',
            'pre_proplayer': '선출 수 (자세하게 적어주세요.)',
        }
        widgets = {
            'team_intro': forms.Textarea(attrs={'rows':2, 'cols':70}),
            'pre_proplayer': forms.Textarea(attrs={'rows':2, 'cols':70}),
        }


class CustomUserCreateForm(UserCreationForm):
    class Meta:
        model = Team
        fields = ['username', 'email', 'password1', 'password2', 'team_name', 'team_logo', 'team_intro', 'region', 'photo', 'gender', 'pre_proplayer']
        labels = {
            'username': '아이디',
            'team_name': '팀 이름',
            'team_logo': '팀 로고 (이미지 첨부파일)',
            'team_intro': '팀 소개 (자세하게 적어주세요.)',
            'region': '지역',
            'photo': '팀 사진 (이미지 첨부파일)',
            'gender': '팀 성별',
            'pre_proplayer': '선출 수 (자세하게 적어주세요.)',
        }
        widgets = {
            'team_intro': forms.Textarea(attrs={'rows':2, 'cols':70}),
            'pre_proplayer': forms.Textarea(attrs={'rows':2, 'cols':70}),
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
        fields = ['title', 'content','image']
        labels = {
            'title' : '제목',
            'content' : '내용',
            'image' : '첨부 이미지',
        }
        
        widgets = {
            'title' : forms.TextInput(attrs={
                    'class' :"form-control",
					'placeholder' : "제목을 입력하세요"}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 20} ),
            'image': forms.FileInput(attrs={'type': 'file'}),
        }


is_matched_list = [(False, "모집중"), (True, "마감됨")]
gender_list = (("male", "남성"), ("female", "여성"), ("mixed", "혼성"))
class MatchFilterForm(forms.ModelForm):
    region = forms.ModelChoiceField(Stadium.objects.values_list('location', flat=True).distinct(), empty_label=None, widget=forms.CheckboxSelectMultiple)
    is_matched = forms.ChoiceField(choices=is_matched_list, widget=forms.CheckboxSelectMultiple)
    gender = forms.ChoiceField(choices=gender_list, widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = MatchInfo
        fields = ['is_matched', 'region', 'gender']
        labels = {
        "region" : "지역",
        'is_matched' : '마감여부',
        'gender' : '성별',
        }
        