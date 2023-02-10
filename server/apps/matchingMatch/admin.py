from django.contrib import admin
from .models import Team, Stadium, MatchInfo, Alarm, Applying_teams

# Register your models here.
admin.site.register(Team)
admin.site.register(Stadium)
admin.site.register(MatchInfo)
admin.site.register(Alarm)
admin.site.register(Applying_teams)

