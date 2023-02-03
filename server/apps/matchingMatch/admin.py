from django.contrib import admin
from .models import Team, User, Stadium, MatchInfo

# Register your models here.
admin.site.register(Team)
admin.site.register(User)
admin.site.register(Stadium)
admin.site.register(MatchInfo)
