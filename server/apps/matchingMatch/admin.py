from django.contrib import admin
from .models import Team, Stadium, MatchInfo, Alarm

# Register your models here.
admin.site.register(Team)
admin.site.register(Stadium)
admin.site.register(MatchInfo)
admin.site.register(Alarm)
